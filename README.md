# DronLomaly: Runtime Log-based Anomaly Detector for DJI Drones

## Anomaly Detector Project

This Python project has 2 functions:
1. Pytorch LSTM model for anomaly detection, and
2. RPC Server at `http://localhost:8000`.

## Telemetry Subscriber Project

This C++ project has 2 functions:
1. OSDK Telemetry data stream from Drone Controller
2. RPC Client sending drone state to `http://localhost:8000`.

To run, navigate to `/path/to/Onboard-SDK/build/bin`, and run `./dji-telemetry-sample UserConfig.txt`

## Rudimentary RPC Client and Server

### RPC Server (Python)

```
import xmlrpc.server

class MyServer:
    def test(self, msg: str):
        print("Received: ", msg)
        return "Hello back from server!"

server = xmlrpc.server.SimpleXMLRPCServer(('localhost', 8000))
server.register_instance(MyServer())
server.serve_forever()
```

### RPC Client (C++)

```
#include <cstdlib>
#include <string>
#include <iostream>
#include <cassert>

using namespace std;

#include <xmlrpc-c/girerr.hpp>
#include <xmlrpc-c/base.hpp>
#include <xmlrpc-c/client_simple.hpp>


int main(int argc, char **){
    xmlrpc_c::clientXmlTransport_curl myTransport(
            xmlrpc_c::clientXmlTransport_curl::constrOpt()
            .timeout(10000)
            .user_agent("test/1.0")
    );
    xmlrpc_c::client_xml myClient(&myTransport);
    
    string const methodName("test");
    
    xmlrpc_c::paramList sampleAddParms;
    sampleAddParms.add(xmlrpc_c::value_string("My"));
    sampleAddParms.add(xmlrpc_c::value_string("Name"));
    sampleAddParms.add(xmlrpc_c::value_string("is"));
    sampleAddParms.add(xmlrpc_c::value_string("Wei"));

    xmlrpc_c::rpcPtr myRpcP(methodName, sampleAddParms);

    string const serverUrl("http://localhost:8000/RPC2");

    xmlrpc_c::carriageParm_curl0 myCarriageParm(serverUrl);
    myRpcP-> call(&myClient, &myCarriageParm);
    assert(myRpcP->isFinished());
}
```

When compiling, you add link the `xmlrpc` modules inside the `g++` command using: 

```
g++ cclient.cc -o cclient.o -lxmlrpc++ -lxmlrpc_client++  -lxmlrpc_util
```

## Steps to modifying the OSDK Telemetry Project 

### Become RPC Client

Navigate to Telemetry module inside OSDK Sample apps, and append following to its `CMakeLists.txt` for RPC Client:

```
target_link_libraries(${PROJECT_NAME} 
xmlrpc++
xmlrpc_client++ 
xmlrpc_util
)
```

### Filesystem Management for Log files
Cast the Unix epoch time to String as the file name of the new log file and create the entire path to the log file: 

```
#include <time.h>
#include <boost/filesystem.hpp>

std::string logPath = "/home/droneteam/Documents/Onboard-SDK/logs/";
boost::filesystem::create_directories(logPath);
std::string fileName = logPath + std::to_string((int)time(NULL)) + "_log.txt";
```

Add `boost_filesystem` and `boost_system` to `target_link_libraries` directive inside `CMakeLists.txt` for creating directory for telemetry log files:
```
target_link_libraries(${PROJECT_NAME} 
xmlrpc++
xmlrpc_client++ 
xmlrpc_util

# for file system management
boost_filesystem
boost_system
)
```

### Stream additional topics

Add `flight_sample.cpp` file from to use the function for converting Quaternion to Euler:
```
FILE(GLOB SOURCE_FILES *.hpp *.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/../common/dji_linux_environment.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/../common/dji_linux_helpers.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/../hal/*.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../osal/*.c

    # for euler angle function
    ${CMAKE_CURRENT_SOURCE_DIR}/../../../core/src/flight_sample.cpp
    )

# for euler angle function
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../../../core/inc)
```

Then install XML RPC files in the Ubuntu development environment: 
```
# sudo apt install libxmlrpc-c++8-dev
```

Afterwards, naviate to `/path/to/Onboard-SDK/build` and compile using `make ;` to update the changes to binaries.