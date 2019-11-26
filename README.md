# PisCeS
Placements are a crucial part of college, yet is often always chaotic and disorganized. In order to provide a seamless and convenient placement experience, we have developed a Placement Coordination System.

The goal of the project is to make the handling of major functionalities regarding placement processes easier for both the students and the placement coordinator.

The features of the system are divided into two broad categories, each having their own components:

<b>User (Student)</b> - The system allows registration for placements,displaying college policies for students, easy one click registration for a particular company which includes eligibility check,displays placement statistics statistics based on tier, company, CTC etc and has a prediction model to predict the CTC of the next company. Company related information is made more accessible and students can use a job search filter to do so and students can even view upcoming events. The entire placement process is made more organised by allowing the user to keep track of the companies visiting along with the dates, provides the necessary venues as well as seating allotments for the students. It also tracks the schedules of the companies visiting. An ‘Alumni Connect’ blog service feature enables users to view previous interview/code experiences of various companies.  Additionally, the system includes a ‘Skill Refinement’ feature that allows the students to hone their skills on several interview-themed subjects.

<b>Admin (Coordinator)</b> - The coordinator can keep track of students placed (and if the student has full time + internship or only full time or only internship). In addition, the system also encompasses an ‘Automail’ feature that automates the process of sending mails to the different companies, as well as updating their responses into the system. The admin will also be allowed to control the pre-placement and venue details via the 'Schedule' feature.

The user logins to the site using their USN/ID and password and new users will be redirected to a separate sign up page. Once logged in, the user can search and find the details of a particular company. The user can view a list of upcoming companies through the Company Tab, company statistics and trends through the Statistics tab, seating allotment and information about the registered companies through a Profile tab and any notifications/updates through a notifications tab.

There are 4 components and 2 interfaces in the Placement Coordination System. The components include :

<b>Browser</b>- It is an application used to access and view the website.

<b>Accounts Application</b> - Contains the login page and password reset page to authenticate users and handle any exceptions by allowing the password to be reset. There are two views for this. One for the admin(placement coordinator) and the other for students. Based on the credentials, the app will redirect to the respective view(studentapp or coordinator app).
Student Application - The students application contains the student dashboard which displays student information and related functionality such as registering, viewing stats etc.

<b>Coordinator Application</b>- The coordination web application is for the placement coordinator where he/she can track the students who are part of the placement cycle. 

<b>Database</b>-Contains all information regarding students and users, companies,labsand seating, scheduling etc. All the other components will query this particular component to display and update data.

The design is based on modularity and information hiding and follows MVC approach.
