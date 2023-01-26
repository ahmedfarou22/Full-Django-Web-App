# IRRIGATION SURPLUS - A SECURE WEB APPLICATION (Full Django WebApp)
## Introduction
For this course work we are asked to develop a secure web application. The web application of
our choice is platform that can help farmers control their water irrigation using data from satellites. As a
team, we had some previous experience in web development since we all were enrolled in a web
development course. In the previous course we used PHP as the back end (server-side language) but in
this project we are planning to use Python and Django. Some of our expected learning outcomes are
learn how to use the Django framework, learn basic/advances web security features, Learn the basics of
penetration testing (test our website), and learn how to work in a team using git version control.

## The Idea 
Maa, the Arabic word for water, is an essential part of our life. Our planet faces many obstacles
in a rapidly evolving world that produces a great amount of waste. It is reported that 70% of humans’
water consumption comes from the agriculture sector, and of that value 40% is lost during the process.
Therefore, we set out to try and alleviate the problem which could potentially save around 30% of the
Earth’s water.
Our solution aims to solve the problem by giving the agricultural industry a platform that can be
used to track the surplus of water for their plots of land. Decreasing the surplus used would greatly help
humans conserve water that might be difficult to come by in areas of the world that suffer from
droughts.
Our platform combines the information from satellite imagery with open-source data (total of 5
data sources) to produce a water surplus that the user should aim to reduce. Two types of satellite
imagery are used to calculate the surplus water. The Sentinel-2 satellite gives us access to the moisture
index in the field being studied. The MODIS satellite gives us access to the potential evapotranspiration
in the area. These two values being plugged in to the moisture index formula (by C. W. Thornthwaite)
𝑚𝑖 =(𝑆−𝐷)/𝑃𝐸𝑇 × 100, would result in getting the surplus water used by the user.
