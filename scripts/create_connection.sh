airflow connections add data_warehouse \
    --conn-type postgres \
    --conn-login $DW_LOGIN \
    --conn-password $DW_PASSWORD \
    --conn-host datawarehouse \
    --conn-port 5432 \
    --conn-schema datawarehouse

# postgresql://$DW_LOGIN:$DW_PASSWORD@datawarehouse:5432/datawarehouse