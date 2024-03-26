How does it look when autonomous cars aren't able to stabilise the system?



https://github.com/sm-bean/CAV-systems-project/assets/148566702/8b5a8bbc-61d2-4427-9387-2dbd7d789a07



In dense environments, autonomous cars can contain traffic waves within the cascade but still fail to completely mitigate them.
In our paper, these situations are also marked as unstable.

https://github.com/sm-bean/CAV-systems-project/assets/148566702/90a08610-a054-407e-b775-1f417e340f10

Here is an example of an INCOMPATIBILITY of the governing equations with obstacles such as traffic lights.

The velocity delta becomes greater than the velocity error causing the autonomous cars to speed through the traffic light.

https://github.com/sm-bean/CAV-systems-project/assets/148566702/acdf3458-568b-42ad-9d8f-1497ea7d39c5

Our simulation can also be used to investigate how phantom traffic behaves. Here we see 4 phantom traffic jams merge into 3, which then merge into 2. 

https://github.com/sm-bean/CAV-systems-project/assets/148566702/7ca33fe3-44d6-4d08-ae92-cea8843d3560

Here we can see how autonomous cars eliminate the traffic waves. (although it fails to stabilise the whole system)

https://github.com/sm-bean/CAV-systems-project/assets/148566702/1fee63f1-4a63-4fea-b7a2-c2580aa2d54b

Our simulation is also able to simulate speed limits. Here is an example of VSL in use, which is mitigating traffic with speed limits. As you can see, it is semi-successful but has a sudden speed difference and is not always stable.



https://github.com/sm-bean/CAV-systems-project/assets/148566702/d21b81ce-0852-4709-9a63-40da753c7509



It's worth noting that VSL also works well in conjuction with CAVs.

https://github.com/sm-bean/CAV-systems-project/assets/148566702/c98a35de-5d86-4fa3-a046-86d5df3ff6a0














