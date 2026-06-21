# ticket-intelligence

A Python script I built to analyze help desk ticket data and generate a weekly PDF report. 

I noticed there was never any visibility into ticket trends at places I've worked — you'd just 
respond to whatever came in with no real way to see patterns. Wanted to build something that 
could answer questions like "what keeps breaking?" and "why does it take so long to fix X?"

## what it does

- generates 500 realistic help desk tickets with randomized categories, priorities, and technicians
- analyzes the data for patterns (top issues, resolution times, busiest days, tech performance)
- spits out a formatted PDF report with charts and actionable recommendations

## why I built it

Mostly to get better at Python and pandas. Also because I think a lot of help desk teams are 
flying blind and a simple report like this could actually change how a team prioritizes work.

## tools used

- Python
- pandas (data analysis)
- matplotlib (charts)
- reportlab (PDF generation)

## sample output

[Ticket_Intelligence_Report.pdf](file:///C:/Users/Admin/Downloads/Ticket_Intelligence_Report%20(2).pdf)

