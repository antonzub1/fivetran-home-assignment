# Local Data Processing Automation Plan

Following things must be taken into account before getting started:
 - current state of automation;
 - who and how are involved in automation;
 - how many resources could be allocated and for how long.

### HVR Hub server
The core of the systems is HVR Hub server which is responsible for channels scheduling and management.
Therefore, it is a great candidate for the start of for tests automation.
HVR hub server encapsulates a functionality which is used by both command line tool and web based interfrace.
Integration tests must be implemented to ensure components work as intended.
Channels management should be addressed as a first point.

### HVR agents
HVR agents work in a distributed environment and act as a producers and consumers of data transferred. Therefore, it is
crucial to have integration tests with some sort of schema / contract for data between them.
Since they can run in distributed mode, which introduces some unique challenges specific only to distributed systems.
Therefore, they have to be addressed acccordingly. Synchronization and consensus algorithms should be verified.
Jepsen is a good tool to test safety of such systems.

### Connectors
HVR Hub server works with various datasources which have their own specifics. Connectors for most popular and critical 
data sources must be tested in a first place.

### Load testing
HVR Hub is intended to manage a lot of channels, therefore load and performance tests should be considered as a way 
of determining limits of the system. k6 will be a great choice for this purpose because it is easy to grasp and start
development, and it has a great integration with existing monitoring tools.

### REST API server
REST API server allows to interact with HVR Hub and control it for the purpose of external usage. REST API is quite
large and covers different aspect of a system, which makes it rather a big milestone in automation. However, tests
developed for this purpose can be easily integrated in further steps or even become a part of the system itself, i.e.
retrieval of agent status, storage connection checks, healthchecks and so on.

### UI Automation
HVR hub has a rich user interface, and will require a lot of effort to automate. However, it's behavior is also covered
by a command line tool with the same functionality, and thus can be de-prioritized for later automation.
Playwright should be taken as a core of UI automation framework since it is mature, well supported, with a supportive
community and does not have problems which selenium had (i.e. waits management)

### Failure management
Such a complex system has a lot of moving parts and is susceptible for unexpected situations despite of all the testing
efforts being put into ensuring it is stable. Therefore, some form of stress or chaos testing can be introduced later in
a lifecycle to ensure that even in the case of a critical failure system can fail in a controllable and graceful way.
Special attention is required for data loss prevention, backups and rollback since these can easily lead to losing a
valuable customer.
