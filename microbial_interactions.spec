/*
A KBase module: microbial_interactions
*/

module microbial_interactions {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_microbial_interactions(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
