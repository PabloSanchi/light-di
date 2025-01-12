## OPTION 1
### Uncomment one of the two following lines to include the respective repository (only one per repository)

import examples.example_3.repository.console_log_repository
# import examples.example_3.repository.simple_log_repository


## OPTION 2
### use the direct container resolver to explicitly include the respective repository
### in this case the use of decorators (for the impls) MUST BE REMOVED otherwise the container will not work 
### as expected

# from lightdi import container
# from examples.example_3.repository.log_repository import LogRepository
# from examples.example_3.repository.console_log_repository import ConsoleLogRepository
# from examples.example_3.repository.simple_log_repository import SimpleLogRepository

## uncomment one of the following lines to include the respective repository (only one per repository)
# container.register_impl(LogRepository, ConsoleLogRepository)
# container.register_impl(LogRepository, SimpleLogRepository)