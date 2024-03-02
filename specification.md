# SEO Analyzer Project

Project on Searching the Web (NDBI038) Summer semester 2023/24.

The project focuses on various aspects of a properly created web page, that can be found by search engines. Properly created is a page that is rated well by the search engines.

## Interface

The tool will be equipped with a graphical user interface, to make it more user-friendly.

The **Frontend** will be created in **React**, with **Material UI** for styling. The first screen will be a simple form where the user can enter the URL to be analysed.

For the **backend** **Flask (Python)** will be used, which is mainly useful for form submission and interaction with the analysis logic.

**Selenium** will be used to perform an analysis of the specified URL.

## Analyzer logic

In the next section, I will introduce you to some logical functions that the app will perform.

**Basic SEO report:** A list of keywords that occur frequently in the text, the length and form of the meta-description and title, the frequency of h1 and h2 headings, the listing of image tags without "alt attribute", the links ratio (internal vs. external links) or broken links

**Other advanced functions:** Search preview, mobile snapshot, canonical tag, page size, response time, disabled Directory Listing, secure connection (https)

## Others

I don't have much experience, so the chosen technologies may not work. But I hope it's ok.

Suggested features (if I'll have enough time or if the mentioned above is not sufficient): Saving the analysis report, suggestions for SEO improvements along each report category.