Vue.component('rule_incompatibility', {
    props: {
        "details": {
            type: Object,

            validator: function (value) {
                // Ensure that the object has all the attributes we need
                if (!value.hasOwnProperty("incompatible_courses")) {
                    value.incompatible_courses = [""];
                }

                return true;
            }
        }
    },
    data: function() {
        return {
            "courses": [],
            "info_msg": INFO_MSGS['course'],

            // Display related warnings if true
            "non_unique_options": false,
            "is_blank": false,

            "redraw": false
        }
    },
    created: function() {
        // Javascript has the best indirection...
        var rule = this;

        var request = new XMLHttpRequest();

        request.addEventListener("load", function() {
            rule.courses = JSON.parse(request.response);
            rule.courses.sort(
                function(a, b){
                    return a['code'].localeCompare(b['code'])
                }
            );

            rule.check_options();
        });
        request.open("GET", "/api/search/?select=code,name&from=course");
        request.send();
    },
    methods: {
        add_course: function() {
            // Mutable modification - redraw needed
            this.details.incompatible_courses.push(-1);
            this.check_options();
            this.do_redraw();
        },
        remove_course: function(index) {
            // Mutable modification - redraw needed
            this.details.incompatible_courses.splice(index, 1);
            this.check_options();
            this.do_redraw();
        },
        check_options: function() {
            // Check for duplicates
            this.non_unique_options = false;
            var found = [];

            for (var index in this.details.incompatible_courses) {
                var value = this.details.incompatible_courses[index];
                if (found.includes(value)) {
                    this.non_unique_options = true;
                    break;
                }
                found.push(value);
            }

            // Ensure all data has been filled in
            this.is_blank = false;
            for (var index in this.details.incompatible_courses) {
                var value = this.details.incompatible_courses[index];
                if (value === -1 || value === "") {
                    this.is_blank = true;
                    break;
                }
            }

            return !this.non_unique_options && !this.is_blank;
        },
        // https://michaelnthiessen.com/force-re-render/
        do_redraw: function() {
            this.redraw = true;

            this.$nextTick(() => {
                this.redraw = false;
            });
        }
    },
    template: '#incompatibilityRuleTemplate'
});
