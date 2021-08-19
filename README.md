# pythonCBReportRefactor

***Welcome!***

Thank you for taking the time to participate in this refactoring project.  This project is not meant to be THE go/no-go in our decision-making process.  Rather, it’s meant as a tool for you to show your way of thinking and a little bit of showing off your Python skills.

Use the following instructions to complete the project.  

***Sample Code***

The Python script provided can be improved in a number of ways.  Also included is a sample output.

***Requirements***

- Testing.  Indicate what changes you have tested and verified, and how you tested and verified them.  Not all is testable, since you don’t have access to the backend RDBMS nor do you know its schema.
- Tools.  Feel free to use whatever IDE you like, whatever imports you fancy and basically whatever gets the job done.  Perhaps the only constraint is to use trusted sources for any libraries.
- Assume the sample Python script will grow in number of queries and reported metrics.  Extend or rework the script to support:
  - More reporting sections without hardcoding each reporting section.  The reporting sections should look the same, though the query and number of columns are unique to each section of output.
  - Configurable date ranges (you might have to adjust the SQL in sample), we might run the report weekly to see #s for the week, or we might change it up to run daily or even monthly.   Since you don’t know the backend RDBMS, it’s ok if the SQL is not perfect/not executable.  
- The script generates a text-only output file.  Revise to output a rich text format that supports images.
- The script does not attempt to protect account names, user names or passwords used to access data sources or email service; all account names, user names and passwords should be protected or at least read into the script vs hardcoded within it.
- As long as we can get the gist of what you're trying to do, it’s good.  This exercise is more about your process, approach and communicating back what you attempted, not Python and SQL syntax.

***Submit***

When you are satisfied with your project, please zip up your project and email it in.
Please do not PR or fork so that we prevent others from seeing your work and copying it 😊
