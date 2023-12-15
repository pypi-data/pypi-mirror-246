from datacentertracesdatasets import loadtraces


trace_name='alibaba2018'
trace_type='machine_usage'
stride_seconds=300
generation_strategy='synthetic'
original_df = loadtraces.get_trace(trace_name, trace_type=trace_type, stride_seconds=stride_seconds, generation_strategy=generation_strategy)
print(original_df)

original_df = loadtraces.get_trace('azure_v2', trace_type=trace_type, stride_seconds=stride_seconds, generation_strategy=generation_strategy)
print(original_df)

original_df = loadtraces.get_trace('google2019', trace_type=trace_type, stride_seconds=stride_seconds, generation_strategy=generation_strategy)
print(original_df)

