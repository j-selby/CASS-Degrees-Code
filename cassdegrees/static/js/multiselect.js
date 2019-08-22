// content for multiselect
// sources (including for HTML and CSS):
// https://vue-multiselect.js.org/#sub-getting-started
// https://medium.com/@hugodesigns/how-to-use-the-most-complete-selecting-solution-for-vue-js-f991b2605364

new Vue({
    // modify delimiters to prevent conflict with Django Template Console
    delimiters: ["[[","]]"],

    components: {
        Multiselect: window.VueMultiselect.default
    },

    data: {
        options: [],
        optionsProxy: [],
        selectedResources: [],
        showLoadingSpinner: false
    },

    http: {
        // Todo: check compatibility against server
        root: 'http://localhost:8000'
    },

    headers:{
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    },

    methods: {
        customLabel (option) {
            return `${option.code} - ${option.name}`
        },

        updateSelected(value) {
            value.forEach((resource) => {
                // Adds selected resources to array
                this.selectedResources.push(resource)
                resourceID = this.options.indexOf(resource)
                this.options.splice(resourceID,1)
            })
            // Clears selected array
            // This prevents the tags from being displayed
            this.optionsProxy = []
            console.log(this.selectedResources.values())
        },

        cdnRequest(value) {
            this.$http.get('api/model/course/').then((response) => {
                // get body data
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
            this.cdnRequest(value)
        },

        removeDependency(index) {
            // when an element is removed from the list, add it back to the options
            this.selectedResources.splice(index, 1).forEach((element) =>{
                this.options.push(element)
            })
        }
    },

    created() {
        const value = ''
        this.cdnRequest(value)
    }

}).$mount('#app')