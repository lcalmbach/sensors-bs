qry = {
    # time_field_name, agg-func, data_table_name, station_table_name, time_value
    'map_data': """select 
	t1.station_id, t2."name" ,t2."lat", t2."long", t1."{0}", {1}(t1."{6}") as value 
    from 
        public."{2}" t1
        inner join public."{3}" t2 on t2.station_id = t1.station_id
    where 
        t2.lat between 46 and 49 and t2.long between 6 and 9 and t1."{0}" = '{4}'
        {5}
    group by 
        t1."station_id", t2."name", t2."lat", t2."long", t1."{0}" """,
    
    # 0:value_field_name, 1:data_table_name, 2:time_field_name 3:time_value
    #'histo_data': """select "{0}" from public."{1}" t1 where t1."{2}" = '{3}'
    #""",

    # 0:time_field, 1:aggregation function, 2:data_table_name, 3:station_table_name
    # 4:time query feld, 5: time_value 6: additional filters
    'time_data_average_all': """select {0}, avg("{6}") as value from 
        public."{1}" t1
        inner join public."{2}" t2 on t2."station_id" = t1."station_id"
    where 
        "{3}" = {4} {5}
    group by "{0}" """,

    # 0: date_column 1: data_table 2: station_table, 3: date_filter_field, 4: date_filter_value, 5: additional filters
    'time_date_stations_raw': """select concat(t1.station_id, ' ', t2."name") as station ,t2."lat", t2."long", t1."{0}", avg(t1."{6}") as value 
        from public."{1}" t1 
        inner join public."{2}" t2 on t2.station_id = t1.station_id 
        where t2.lat > 40 and t1."{3}" = '{4}' 
        {5} 
        group by concat(t1.station_id, ' ', t2."name"), t2."lat", t2."long", t1."{0}" """,

    'min_max_time': """select min(date) as min, max(date) as max from public."{}" """,

    'stations_all': """select *, CONCAT(station_id, ' - ' , name) as id_name from public."{}" 
        where lat between 46 and 49 and long between 6 and 9 order by station_id;""",

    # 0: aggregation date, 1: 1: labe, e.g. concat(year, 'week'), 2: data table
    'date_aggregation_list': """select distinct {0} as "key", {1} as "value" from  public."{2}" 
    where {0} is not null
    order by {0} asc""",

    'no_stations_query': """select count(*) as value from public."{}"
    """


}