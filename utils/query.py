QUERY_PRESENTACIONES = """/*
Reporte de Prestaciones y productos que no ingresaron a un CUENTA
y cuya liquidacion esta en situacion de FINALIZADO 
*/

let mz = Ax.db.execute
(`
SELECT  'PRES' AS TIPO,
        PRES.acp_episodio AS EPISODIO,        
        LIQ.liq_financiador AS COD_FINANCIADOR,
        FIN.fin_razon_social AS DESC_FINANCIADOR,        
        TFIN.tfin_nombre AS TIPO_FINANCIADOR,
        TCONT.tipc_nombre as TIPO_CONTRATO,
        TLIQ.liqt_descripcion as TIPO_LIQUIDACION,
        LIQ.liq_ambito as AMBITO,
        LIQ.liq_numero as NUMERO_LIQ,  
        LIQV.liqver_numver AS VERS_LIQ,      
        CUENTA.cnt_numero as CUENTA_LIQ,
        CASE WHEN LIQ.liq_estdoc = 'A' THEN 'APROBADO'
             WHEN LIQ.liq_estdoc = 'C' THEN 'COBRO DE EJECUCION'
             WHEN LIQ.liq_estdoc = 'F' THEN 'FINALIZADO'
             WHEN LIQ.liq_estdoc = 'G' THEN 'VIGENCIA ACTIVA'
             WHEN LIQ.liq_estdoc = 'N' THEN 'NO FACTURABLE'
             WHEN LIQ.liq_estdoc = 'O' THEN 'OBSERVADO'
             WHEN LIQ.liq_estdoc = 'P' THEN 'PENDIENTE'
             WHEN LIQ.liq_estdoc = 'R' THEN 'PENDIENTE DE FACTURACION'
             WHEN LIQ.liq_estdoc = 'S' THEN 'SOLICITUD ENVIADA'
             WHEN LIQ.liq_estdoc = 'T' THEN 'EN AUDITORIA'
             WHEN LIQ.liq_estdoc = 'V' THEN 'VALIDADO'
             ELSE 'NO DEFINIDO'
        END AS SITUACION_LIQ,
        CASE WHEN LIQ.liq_estado = 'A' THEN 'ABIERTO'
             WHEN LIQ.liq_estado = 'C' THEN 'CERRADO'
             WHEN LIQ.liq_estado = 'N' THEN 'ANULADO'
             WHEN LIQ.liq_estado = 'F' THEN 'FACTURADO'
             ELSE 'NO DEFINIDO'
        END AS ESTADO_LIQ,
        PRES.acp_paciente AS HC,
        NVL(PAC.pac_apellido1,'') || ' ' || NVL(PAC.pac_apellido2,'') || ' ' || NVL(PAC.pac_nombre,'') AS NOMBRE_PACIENTE,
        DATE(PRES.acp_fecha) AS FECHA_CONSUMO,
        PRES.acp_presta_acto AS CODIGO,        
        TPRES.pre_nombre AS DESCRIPCION,        
        PRES.acp_concep_fact AS CONCEP_FACTURABLE,
        CFACT.cfa_nombre as NOMBRE_CONCEP_FACTURABLE,
        PRES.acp_origen_app AS ORIGEN,        
        CASE WHEN PRES.acp_estado = 'S' THEN 'Sustituido'
            WHEN PRES.acp_estado = 'V' THEN 'Valorado'
            WHEN PRES.acp_estado = 'L' THEN 'Liquidado'
            WHEN PRES.acp_estado = 'A' THEN 'Anulado'
            WHEN PRES.acp_estado = 'N' THEN 'No facturable'
            WHEN PRES.acp_estado = 'R' THEN 'Registrado'
            WHEN PRES.acp_estado = 'T' THEN 'Traslado consumos'
            WHEN PRES.acp_estado = 'U' THEN 'Traslado Emergencia'
            WHEN PRES.acp_estado = 'P' THEN 'En paquete'
            WHEN PRES.acp_estado = 'G' THEN 'Agrupador paquete'
            WHEN PRES.acp_estado = 'Z' THEN 'Paquete anulado'
            WHEN PRES.acp_estado = 'D' THEN 'Descartado'
        END AS ESTADO_CONSUMO,
        PRES.acp_cantidad AS CANTIDAD,
        PRES.acp_precio_tar AS PRECIO_FACTURABLE,
        PRES.acp_importe_neto AS IMPORTE_BRUTO,
        PRES.acp_origen_doc AS GUIA        
        FROM fas_actividad_pres PRES LEFT JOIN fas_admision as ADM on ADM.adm_episodio = PRES.acp_episodio
                                     LEFT JOIN fas_liquidacion as LIQ on LIQ.liq_episodio = ADM.adm_episodio
                                     LEFT JOIN fas_liquidacion_tipo as TLIQ on TLIQ.liqt_codigo = LIQ.liq_tipo
                                     LEFT JOIN fas_paciente as PAC on PAC.pac_historia_clinica = PRES.acp_paciente
                                     LEFT JOIN fas_concepto_facturable as CFACT on CFACT.cfa_codigo = PRES.acp_concep_fact
                                     LEFT JOIN fas_prestacion as TPRES on TPRES.pre_codigo = PRES.acp_presta_acto                                     
                                     LEFT JOIN fas_financiador AS FIN       on FIN.fin_codigo = LIQ.liq_financiador
                                     LEFT JOIN fas_tipo_financiador AS TFIN     on TFIN.tfin_codigo = FIN.fin_tipo_financiador
                                     LEFT JOIN fas_tipo_contrato AS TCONT    on TCONT.tipc_codigo = FIN.fin_tipo_contrato
                                     LEFT JOIN fas_cuenta AS CUENTA         on CUENTA.CNT_ID = LIQ.liq_cnt_id   
                                     LEFT JOIN fas_liquidacion_vers LIQV on LIQV.liq_id = LIQ.liq_id                                     
        WHERE PRES.acp_estado IN ('V', 'R', 'T')
              AND ADM.adm_estado = 'V' 
              AND acp_cuenta_id IS NULL
              
              AND LIQ.Liq_tipo <> '00'
              and LIQV.liqver_id = (SELECT MAX(flv.liqver_id)
											FROM fas_liquidacion_vers flv
										   WHERE flv.liq_id = LIQ.liq_id) 
              AND LIQ.liq_estdoc = 'F'
              AND LIQ.liq_financiador in ('00061540','00060990')
UNION ALL

SELECT  'PROD' AS TIPO,
        PROD.acd_episodio AS EPISODIO,        
        LIQ.liq_financiador AS COD_FINANCIADOR,
        FIN.fin_razon_social AS DESC_FINANCIADOR,        
        TFIN.tfin_nombre AS TIPO_FINANCIADOR,
        TCONT.tipc_nombre as TIPO_CONTRATO,
        TLIQ.liqt_descripcion as TIPO_LIQUIDACION,
        LIQ.liq_ambito as AMBITO,
        LIQ.liq_numero as NUMERO_LIQ,  
        LIQV.liqver_numver AS VERS_LIQ,
        CUENTA.cnt_numero as CUENTA_LIQ,
        CASE WHEN LIQ.liq_estdoc = 'A' THEN 'APROBADO'
             WHEN LIQ.liq_estdoc = 'C' THEN 'COBRO DE EJECUCION'
             WHEN LIQ.liq_estdoc = 'F' THEN 'FINALIZADO'
             WHEN LIQ.liq_estdoc = 'G' THEN 'VIGENCIA ACTIVA'
             WHEN LIQ.liq_estdoc = 'N' THEN 'NO FACTURABLE'
             WHEN LIQ.liq_estdoc = 'O' THEN 'OBSERVADO'
             WHEN LIQ.liq_estdoc = 'P' THEN 'PENDIENTE'
             WHEN LIQ.liq_estdoc = 'R' THEN 'PENDIENTE DE FACTURACION'
             WHEN LIQ.liq_estdoc = 'S' THEN 'SOLICITUD ENVIADA'
             WHEN LIQ.liq_estdoc = 'T' THEN 'EN AUDITORIA'
             WHEN LIQ.liq_estdoc = 'V' THEN 'VALIDADO'
             ELSE 'NO DEFINIDO'
        END AS SITUACION_LIQ,
        CASE WHEN LIQ.liq_estado = 'A' THEN 'ABIERTO'
             WHEN LIQ.liq_estado = 'C' THEN 'CERRADO'
             WHEN LIQ.liq_estado = 'N' THEN 'ANULADO'
             WHEN LIQ.liq_estado = 'F' THEN 'FACTURADO'
             ELSE 'NO DEFINIDO'
        END AS ESTADO_LIQ,
        PROD.acd_paciente AS HC,
        NVL(PAC.pac_apellido1,'') || ' ' || NVL(PAC.pac_apellido2,'') || ' ' || NVL(PAC.pac_nombre,'') AS NOMBRE_PACIENTE,
        DATE(PROD.acd_fecha) AS FECHA_CONSUMO,
        PROD.acd_producto AS CODIGO,        
        TPRES.prd_nombre AS DESCRIPCION,        
        PROD.acd_conc_fact AS CONCEP_FACTURABLE,
        CFACT.cfa_nombre as NOMBRE_CONCEP_FACTURABLE,
        PROD.acd_origen_app AS ORIGEN,
        CASE WHEN PROD.acd_estado = 'S' THEN 'Sustituido'
            WHEN PROD.acd_estado = 'V' THEN 'Valorado'
            WHEN PROD.acd_estado = 'L' THEN 'Liquidado'
            WHEN PROD.acd_estado = 'A' THEN 'Anulado'
            WHEN PROD.acd_estado = 'N' THEN 'No facturable'
            WHEN PROD.acd_estado = 'R' THEN 'Registrado'
            WHEN PROD.acd_estado = 'T' THEN 'Traslado consumos'
	        WHEN PROD.acd_estado = 'U' THEN 'Traslado Emergencia'
	        WHEN PROD.acd_estado = 'P' THEN 'En paquete'
	        WHEN PROD.acd_estado = 'G' THEN 'Agrupador paquete'
	        WHEN PROD.acd_estado = 'Z' THEN 'Paquete anulado'
	        WHEN PROD.acd_estado = 'D' THEN 'Descartado'
        END AS ESTADO_CONSUMO,
        PROD.acd_cantidad AS CANTIDAD,
        PROD.acd_precio_tar AS PRECIO_FACTURABLE,
        PROD.acd_importe_bruto AS IMPORTE_BRUTO,
        PROD.acd_origen_doc AS GUIA        
        FROM fas_actividad_prod PROD LEFT JOIN fas_admision as ADM on ADM.adm_episodio = PROD.acd_episodio
                                     LEFT JOIN fas_liquidacion as LIQ on LIQ.liq_episodio = ADM.adm_episodio
                                     LEFT JOIN fas_liquidacion_tipo as TLIQ on TLIQ.liqt_codigo = LIQ.liq_tipo
                                     LEFT JOIN fas_paciente as PAC on PAC.pac_historia_clinica = PROD.acd_paciente
                                     LEFT JOIN fas_concepto_facturable as CFACT on CFACT.cfa_codigo = PROD.acd_conc_fact
                                     LEFT JOIN fas_producto as TPRES on TPRES.prd_codigo = PROD.acd_producto                                     
                                     LEFT JOIN fas_financiador AS FIN       on FIN.fin_codigo = LIQ.liq_financiador
                                     LEFT JOIN fas_tipo_financiador AS TFIN     on TFIN.tfin_codigo = FIN.fin_tipo_financiador
                                     LEFT JOIN fas_tipo_contrato AS TCONT    on TCONT.tipc_codigo = FIN.fin_tipo_contrato
                                     LEFT JOIN fas_cuenta AS CUENTA         on CUENTA.CNT_ID = LIQ.liq_cnt_id   
                                     LEFT JOIN fas_liquidacion_vers LIQV on LIQV.liq_id = LIQ.liq_id                                     
        WHERE PROD.acd_estado IN ('V', 'R', 'T')
              AND ADM.adm_estado = 'V' 
              AND acd_cuenta_id IS NULL
              
            AND LIQ.Liq_tipo <> '00'
            and LIQV.liqver_id = (SELECT MAX(flv.liqver_id)
											FROM fas_liquidacion_vers flv
										   WHERE flv.liq_id = LIQ.liq_id)
            AND LIQ.liq_estdoc = 'F'
            AND LIQ.liq_financiador in ('00061540','00060990')
into temp @tmpMatriz;
`)

let cns = Ax.db.executeQuery
(`
    select @tmpMatriz.* from @tmpMatriz order by episodio,tipo
`)
return cns

"""