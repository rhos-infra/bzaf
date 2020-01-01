==========
Quickstart
==========

Regular usage::

    git clone https://github.com/rhos-infra/bzaf.git
    cd bzaf
    virtualenv venv_bzaf
    pip install .

Example run::

    Run on a single bz:
    bzaf --debug --fatal --bugzilla \
    https://partner-bugzilla.redhat.com \
    --access-api-key **** --bzid 1618759 \
    --current-status ON_QA \
    --verified-status VERIFIED \
    --verified-resolution VERIFIED \
    --job-env 'pidone,3cont_2comp'

    Run on Multiple bz's query:
    bzaf --debug --fatal \
    --bugzilla https://partner-bugzilla.redhat.com \
    --access-api-key **** \
    --current-status ON_QA --verified-status VERIFIED --verified-resolution VERIFIED \
    --job-env 'pidone,3cont_2comp' \
    --bz-query='https://partner-bugzilla.redhat.com/buglist.cgi?bug_severity=unspecified&bug_severity=urgent&bug_severity=high&bug_status=ON_QA&classification=Red%20Hat&columnlist=bug_\
    status%2Cshort_desc%2Cbug_id&f1=cf_internal_whiteboard&known_name=all%20ON_QA%20pidone&list_id=10116655&o1=substring&priority=unspecified&priority=urgent&priority=high&query_\
    based_on=all%20ON_QA%20pidone&query_format=advanced&v1=DFG%3APIDONE'

Via Infrared Plugin::

    Install Infrared:
    https://infrared.readthedocs.io/en/latest/setup.html

    Add Bzaf as Infrared Plugin:
    git clone https://github.com/rhos-infra/bzaf.git
    ir plugin add https://github.com/rhos-infra/bzaf.git
    ir bzaf -vv \
    --bzaf_cmd_attrd " --debug --fatal \
    --bugzilla https://partner-bugzilla.redhat.com \
    --access-api-key **** \
    --current-status ON_QA --verified-status VERIFIED --verified-resolution VERIFIED \
    --job-env 'pidone,3cont_2comp' \
    --bz-query='https://partner-bugzilla.redhat.com/buglist.cgi?bug_severity=unspecified&bug_severity=urgent&bug_severity=high&bug_status=ON_QA&classification=Red%20Hat&columnlist=bug_\
    status%2Cshort_desc%2Cbug_id&f1=cf_internal_whiteboard&known_name=all%20ON_QA%20pidone&list_id=10116655&o1=substring&priority=unspecified&priority=urgent&priority=high&query_\
    based_on=all%20ON_QA%20pidone&query_format=advanced&v1=DFG%3APIDONE'"


