**DegreeFinder**

**App Overview**
- helps Bentley University students chose their degree by selecting classes that interest them

**App Features**
- checkboxes of classes (with hovering tooltip to view class descriptions and dropdown to filter classes)
- barcharts to display percent degree matches
- lists to display percent degree matches (with hovering toolip and hyperlink to view major / minor descriptions)

**App Files**
- **CourseAZLinks:** gets class code urls (ie. https://catalog.bentley.edu/undergraduate/courses/ac/)
- **CourseDescriptions:** gets course descriptions
- **CourseDepartment:** gets course departments
- **DegreeLinksList:** gets degree urls (ie. https://catalog.bentley.edu/undergraduate/programs/business-programs/accountancy-major/)
- **DegreeLinksDict:** gets degrees + degree urls (ie. 'Accounting Major (B.S.)': 'https://catalog.bentley.edu/undergraduate/programs/business-programs/accountancy-major/')
- **DegreeReq:** gets degree requirements (classes within "major courses") (ie. {'Accounting Major (B.S.)': ['Preparing and Interpreting Financial Statements', 'Performance Measurement', 'Cost Management', 'Financial Accounting and Reporting I', 'Financial Accounting and Reporting II', 'Accounting Information Systems', 'Federal Taxation', 'Financial Statement Auditing', 'Internal Auditing'])
- **StreamlitApp:** creates user interface (checkboxes, percent degree match calculation, barcharts, lists) 
  
**Maintenance**
- if the webscraping from the different App Files does not work (would only occur if Bentley University changed the format of their websites), comment out the code and instead use the hard-coded value(s) at the bottom of the page
- if the app "sleeps" (would only occur due to 24+ hours of inactivity), the user themsevles can wake the app up 
