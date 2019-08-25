// content for multiselect
// sources (including for HTML and CSS):
// https://vue-multiselect.js.org/#sub-getting-started
// https://medium.com/@hugodesigns/how-to-use-the-most-complete-selecting-solution-for-vue-js-f991b2605364

new Vue({
    // modify delimiters to prevent conflict with Django Template Console
    delimiters: ["[[","]]"],

    // el: #app,

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
    headers:{
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    },

    methods: {
        // The label that will be displayed on the list item
        customLabel (option) {
            return `${option.code} - ${option.name}`
        },

        // Update an array of selected values and remove the selected item from the list of available options
        updateSelected(value) {
            value.forEach((resource) => {
                // Adds selected resources to array
                console.log("active element in updateSelected: " + document.activeElement)

                this.selectedResources.push(resource)
                resourceID = this.options.indexOf(resource)
                document.getElementById("id_elements").value = JSON.stringify(this.selectedResources)
                this.options.splice(resourceID,1)
            })

            // Clear options proxy to avoid selection tags from being displayed
            this.optionsProxy = []
            console.log(this.selectedResources.values())
        },

        reactivateeWindow(e){
            // this.$refs.multiselectref.$el.focus()
            console.log("reactivate window called: " + document.activeElement)

        },

        courseRequest(value) {
            // Todo: adjust implementation to cater for generalisation of multiselect beyond courses
            this.$http.get('api/model/course/').then((response) => {

                // get all element data
                this.options = []
                console.log(response.body)
                response.body.forEach((object) => {
                    this.options.push(object)
                });

                this.showLoadingSpinner = false
            }, (response) => {
                // error callback
            })
        },

        searchQuery(value) {
            this.showLoadingSpinner = true
            // GET
            this.courseRequest(value)
        },

        // remove the item from the display list and the elements field when x is clicked
        removeDependency(index) {
            // when an element is removed from the list, add it back to the options
            this.selectedResources.splice(index, 1).forEach((element) =>{
                this.options.push(element)
            })
            document.getElementById("id_elements").value = JSON.stringify(this.selectedResources)
        },


    },

    created() {
        const value = ''
        this.courseRequest(value)
        existingElements = JSON.parse(document.getElementById("id_elements").value)
        existingElements.forEach((object) => {
            this.updateSelected(object)
        })
    },

}).$mount('#app')