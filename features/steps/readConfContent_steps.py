from behave import given, when, then, step
from configparser import SafeConfigParser
from PythonConfluenceAPI import ConfluenceAPI
import pypandoc
import re

def setupAPI():
    #Read the config file
    config = SafeConfigParser()
    config.read('config.ini')

    username = config.get('main', 'USERNAME')
    password = config.get('main', 'PASSWORD')
    wiki_site = config.get('main', 'WIKI_SITE')

    global wikiPageTitle
    wikiPageTitle = config.get('main', 'WIKI_PAGE_TITLE')

    # Setup the Confluence API call
    global api
    api = ConfluenceAPI(username, password, wiki_site)

@given(u'I have Confluence user credentials')
def step_impl(context):
    setupAPI()

@when(u'I look for a wiki page with a specific title')
def step_impl(context):
    global wiki_page
    wiki_page = api.get_content(title=wikiPageTitle, expand="body.view")

@then(u'I want the be able to extract the content')
def step_impl(context):
    global wikiPageContentValue
    dictKeys = wiki_page.keys()

    if 'results' in wiki_page:
        dictResults = wiki_page.get('results')

        dictIndictResults = dictResults[0]

        if 'body' in dictIndictResults:
            bodyOfPage = dictIndictResults.get('body')

            if 'view' in bodyOfPage:
                viewElements = bodyOfPage.get('view')

                if 'value' in viewElements:
                    wikiPageContentValue = viewElements.get('value')

    else:
        print("wikiPageTitle does not have any content to extract")

@given(u'I have a Confluence page wiki content')
def step_impl(context):
    # Replacing spaces with an underscore in the wikiPageTitle name,
    # to get it ready for the name of the tex file.
    global texFileName
    texFileName = wikiPageTitle.replace (" ", "_")


@when(u'the content is converted to a workable tex format')
def step_impl(context):
    # NOTE: pandoc uses \tightlist in list which means a macro
    # \def\tightlist{} needs to be added to the resulting latex infrastructure.
    # TODO: check the resulting tex file for and \href instances as these should not
    # be in here.
    # output = pypandoc.convert_text(wikiPageContentValue, 'tex', format='html', outputfile=texFileName+".tex")
    global rawTex
    rawTex = pypandoc.convert_text(wikiPageContentValue, 'tex', format='html')

@then(u'sanitize the content to be ready for final document format')
def step_impl(context):
    # NOTE: the subsections cause a little trouble for the resulting template LATEX ToC
    # and so it's better to convert all \subsections to \subsections* and \subsubsection
    # to \subsubsection*. This will mean the subsections are NOT numbered.

    outputTex = re.sub(r'\\section', '\section*', rawTex)
    outputTex = re.sub(r'\\subsection', '\subsection*', outputTex)
    outputTex = re.sub(r'\\subsubsection', '\subsubsection*', outputTex)

    tex_file = open(texFileName+".tex", "w")
    tex_file.write(outputTex)
    tex_file.close()
