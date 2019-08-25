// content for multiselect
// sources (including for HTML and CSS):
// https://vue-multiselect.js.org/#sub-getting-started
// https://medium.com/@hugodesigns/how-to-use-the-most-complete-selecting-solution-for-vue-js-f991b2605364

API_MODEL_URL = 'api/model/course/'

new Vue({
    // modify delimiters to prevent conflict with Django Template Console
    delimiters: ["[[", "]]"],

    el: '#app',

    components: {
        Multiselect: window.VueMultiselect.default
    },

    data: {
        options: [],
        optionsProxy: [],
        selectedResources: [],
        showLoadingSpinner: false
    },

    // http element used for constructing API call in courseRequest
    http: {
        // Todo: check compatibility against server
        root: 'http://localhost:8000'
    },

    // Todo: check whether this is required
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    },

    methods: {
        // Todo check what this is doing
        // The label that will be displayed on the list item
        customLabel(option) {
            return `${option.code} - ${option.name}`
        },

        // todo: check for ways to conceal dropdown until user enters input
        // check for input and keep dropdown closed if none
        // checkForInput(){
        //     if (this.value == null) {
        //         this.$refs.multiselectref.maxHeight = 0
        //     } else {
        //         this.$refs.multiselectref.maxHeight = 300
        //     }
        // },

        // Update an array of selected values and remove the selected item from the list of available options
        updateSelected(value) {
            value.forEach((resource) => {
                // Adds selected resources to array

                // only add selection if not already contained in the list
                if (!this.selectedResources.some(element => element.code === resource.code)) {
                    this.selectedResources.push(resource)

                    // sort course listing by course code
                    // https://flaviocopes.com/how-to-sort-array-of-objects-by-property-javascript/
                    this.selectedResources.sort((a, b) => (a.code > b.code) ? 1 : -1)

                    // set the hidden elements form box to value of selectedResources
                    document.getElementById("id_elements").value = JSON.stringify(this.selectedResources)

                    resourceID = this.options.indexOf(resource)
                    this.options.splice(resourceID, 1)
                }
            })

            // Clear options proxy to avoid selection tags from being displayed
            this.optionsProxy = []

        },

        courseRequest(value) {
            // Todo: adjust implementation to cater for generalisation of multiselect beyond courses
            this.$http.get(API_MODEL_URL).then((response) => {

                // get all element data
                this.options = []
                this.selectedResources = []
                response.body.forEach((object) => {
                    this.options.push(object)
                });

                this.showLoadingSpinner = false

                // create objects from existing data if present and load those into the ul element
                existingElements = JSON.parse(document.getElementById("id_elements").value)
                existingElements.forEach((object) => {
                    this.selectedResources.push(object)
                })

            }, (response) => {
                // error callback
            })
        },

        // remove the item from the display list and the elements field when x is clicked
        removeDependency(index) {
            // when an element is removed from the list, add it back to the options
            this.selectedResources.splice(index, 1).forEach((element) => {
                this.options.push(element)
            })
            document.getElementById("id_elements").value = JSON.stringify(this.selectedResources)
        },
    },

    created() {
        const value = ''
        this.courseRequest(value)
    },

}).$mount('#app')