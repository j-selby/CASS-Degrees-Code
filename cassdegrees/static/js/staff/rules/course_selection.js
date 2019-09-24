Vue.component('rule_course_list', {
    props: {
        "details": {
            type: Object,

            validator: function (value) {
                // Ensure that the object has all the attributes we need
                if (!value.hasOwnProperty("codes")) {
                    value.codes = [];
                }

                if (!value.hasOwnProperty("list_type")) {
                    // possible values = LIST_TYPES
                    value.list_type = "";
                }

                if (!value.hasOwnProperty("unit_count")) {
                    value.unit_count = "0";
                }

                return true;
            }
        },
    },

    // subcomponent of the selector must be declared and included in rulescripts.html
    components: {
        Multiselect: window.VueMultiselect.default
    },

    data: function() {
        return {
            "courses": [],          // used to store options for display - details.codes is used for database storage of selected course codes
            "list_types": [],
            "selected_courses": [], // used to store the code and name version of the course when selected
            "coursename_dict": {},  // used to store and find course names so background database not affected by selections
            "optionsProxy": [],     // required prop, default behaviour to display selection tags
            "lists": [],            // stores database lists for display if required
            "tempStore": [],        // holds course options when list selection is in use
            "showLoadingSpinner": false,
            "info_msg": INFO_MSGS['course'],

            // Display related warnings if true
            "non_unique_options": false,
            "invalid_units": false,
            "invalid_units_step": false,
            "is_blank": false,

            // Track whether adding list
            "is_list_search": false,

            "redraw": false
        }
    },
    created: function() {
        var rule = this;
        var request = new XMLHttpRequest();

        // add available courses
        request.addEventListener("load", function() {
            rule.courses = JSON.parse(request.response);
            rule.sortCourseOptions();

            // populate a name dictionary to reconcile selected codes with names without an additional API call
            rule.courses.forEach((courseObj) => {
                rule.coursename_dict[courseObj.code] = courseObj.name
            });

            rule.list_types = LIST_TYPES;
            rule.check_options();

            // if there are already selected courses in details.codes when the component is loaded load,
            // remove them from the options - must be done after courses response received
            if (!(rule.details.codes.length === 0)) {
                for (let i = 0; i < rule.details.codes.length; i++){
                    for (let x = 0; x < rule.courses.length; x++){
                        if (rule.courses[x].code === rule.details.codes[i]['code']) {
                            rule.courses.splice(x, 1).forEach(course => {
                                rule.selected_courses.push(course)
                            });
                            break;
                        }
                    }
                }
            }
        });

        request.open("GET", "/api/search/?select=code,name&from=course");
        request.send();


        // Keep a copy of the Or Rule's "count_units" function (Or a blank function if unavailable)
        this.parent_count_units_fn = this.$parent.get_or_rule_count_units_fn();
    },

    computed: {
        // generates the appropriate placeholder text for the tool depending on list or course mode
        placeholderText(){
            return this.is_list_search ? "Search lists..." : "Search courses, press esc or tab to close when done"
        },

        // used to compute appropriate ordering for template ul element
        sortedSelectedList(){
            return this.selected_courses.sort((a, b) => (a.code > b.code) ? 1 : -1)
        },

        // used to compute appropriate ordering for dropdown list
        sortedCourseList(){
            return this.courses.sort((a, b) => (a.code > b.code) ? 1 : -1)
        },

    },

    methods: {
        // Returns label for multiselect drop down, label for dynamic list beneath generated separately
        customLabel(option) {
            if (this.is_list_search) {
                return `${option.name} - ${option.year}`
            } else {
                return `${option.code} - ${option.name}`
            }
        },

        // force sort of multiselect options list on refresh
        sortCourseOptions(){
            this.courses = this.sortedCourseList
        },

        toggleListMode(){
            if (this.is_list_search) {
                this.is_list_search = false;
                this.courses = this.tempStore;
                this.tempStore = []
            } else {
                // track that the input has changed to list mode
                this.is_list_search = true;

                // preserve the list of course options
                this.tempStore = this.courses;

                // get available lists from database
                var rule = this;
                var request = new XMLHttpRequest();

                request.addEventListener("load", function () {
                    rule.lists = JSON.parse(request.response);
                    rule.lists.sort(
                        function (a, b) {
                            return a['name'].localeCompare(b['name'])
                        }
                    );
                    rule.courses = rule.lists
                });

                request.open("GET", "/api/search/?select=name,year,elements&from=list");
                request.send();
            }
        },

        // Update an array of selected values and remove the selected item from the list of available options
        // Will distinguish between adding an existing list and adding a course
        updateSelected(value) {
            if (this.is_list_search) {
                value.forEach((list) => {
                    list.elements.forEach((course) => {
                        // add course code to details.codes if not already present
                        if (!this.details.codes.some(code => code === course.code)) {
                            this.details.codes.push({'code': resource.code, 'name': resource.name})
                        }

                        // if a course is added through a list, remove it from the temporary store of courses
                        for (let i = 0; i < this.tempStore.length; i++) {
                            if (this.tempStore[i].code === course.code) {
                                this.tempStore.splice(i, 1).forEach(option => {
                                    this.selected_courses.push(option);
                                });
                                break;
                            }
                        }
                    })
                });

                // switch off list mode
                this.toggleListMode()

            } else {
                value.forEach((resource) => {
                    // Adds selected resources to array and prevents duplicates
                    if (!this.details.codes.some(code => code === resource.code)) {
                        this.selected_courses.push(resource)
                        this.details.codes.push({'code': resource.code, 'name': resource.name});
                    }
                    // remove the selected course from the list of available courses to add
                    let resourceID = this.courses.indexOf(resource)
                    this.courses.splice(resourceID, 1)
                });
            }

            // Clear options proxy to avoid selection tags from being displayed
            this.optionsProxy = []
        },

        // remove the item from the display list and the elements field when x is clicked
        // index is the index from the selected_courses array
        // remove code details.codes
        removeDependency(index) {
            this.selected_courses.splice(index, 1).forEach((course) => {
                // add deleted course back to options
                this.courses.push(course)
                this.sortCourseOptions()

                // find and remove code from details.codes
                for (let i = 0; i < this.details.codes.length; i++){
                    if (course.code === this.details.codes[i]['code']){
                        this.details.codes.splice(i, 1);
                        break;
                    }
                }
            });

            this.check_options();
            this.do_redraw();
        },

        check_options: function() {
            // Ensure all data has been filled in
            this.is_blank = this.details.unit_count == null;
            this.is_blank = this.details.codes.length === 0;
            this.is_blank = this.is_blank || this.details.list_type === "";

            // Duplicates are prevented by condition on updateSelected()

            // Ensure Unit Count is valid:
            if (this.details.unit_count != null) {
                this.invalid_units = this.details.unit_count <= 0;
                this.invalid_units_step = this.details.unit_count % 6 !== 0;
            }

            return !this.invalid_units && !this.invalid_units_step && !this.is_blank;
        },

        update_units: function() {
            // To be called whenever the unit count is updated. Will ask the OR rule to re-evaluate the unit count
            this.parent_count_units_fn();
            this.check_options();
        },
        // https://michaelnthiessen.com/force-re-render/
        do_redraw: function() {
            this.redraw = true;

            this.$nextTick(() => {
                this.redraw = false;
            });
        }
    },
    template: '#course-list-template'
});
