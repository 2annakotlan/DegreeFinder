**DegreeFinder**

**App Overview**
helps Bentley University students chose their major & minor by selecting classes that interest them

**App Features**
- checkboxes of classes (with hovering tooltip to view class descriptions)
- barcharts to display percent degree matches
- lists to display percent degree matches (with hovering toolip and hyperlink to view major & minor descriptions)

**App Files**
- **CourseAZLinks:** gets urls for each class code (ie. https://catalog.bentley.edu/undergraduate/courses/ac/)
- **CourseDescriptions:** uses CourseAZLinks to get course descriptions
  
- **DegreeLinksList:** gets urls for each major (ie. https://catalog.bentley.edu/undergraduate/programs/business-programs/accountancy-major/)
- **DegreeLinksDict:** uses DegreeLinksList to get a major:major_url(ie. 'Accounting Major (B.S.)': 'https://catalog.bentley.edu/undergraduate/programs/business-programs/accountancy-major/')
- DegreeReq: uses 
