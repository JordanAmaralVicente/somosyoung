airflow connections add data_warehouse \
    --conn-type postgres \
    --conn-login $DW_LOGIN \
    --conn-password $DW_PASSWORD \
    --conn-host datawarehouse \
    --conn-port 5432 \
    --conn-schema datawarehouse

# postgresql://$DW_LOGIN:$DW_PASSWORD@datawarehouse:5432/datawarehouse

airflow connections add ahoy_viewer_ti \
    --conn-type http \
    --conn-host app.alunos.me \
    --conn-schema https \
    --conn-extra '{"token": "G5n2w1lm*eJF$UukF5c^bN5Re#"}'
