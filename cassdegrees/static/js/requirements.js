//! Vue.js based means of adding/removing requirements.

// Translation table between internal names for components and human readable ones.
const COMPONENT_NAMES = {
    'course': "Course"
};

Vue.component('requirement_course', {
    props: {
        "details": {
            type: Object,

            validator: function (value) {
                // Ensure that the object has all the attributes we need
                if (!value.hasOwnProperty("ids")) {
                    value.ids = [-1];
                }

                return true;
            }
        }
    },
    data: function() {
        return {
            "courses": [],

            // Display related warnings if true
            "non_unique_options": false,

            "invalid_units": false,
            "invalid_units_step": false,

            "redraw": false
        }
    },
    created: function() {
        // Javascript has the best indirection...
        var rule = this;

        var request = new XMLHttpRequest();

        request.addEventListener("load", function() {
            rule.courses = JSON.parse(request.response);

            rule.check_options();
        });
        request.open("GET", "/api/model/course/?format=json");
        request.send();
    },
    methods: {
        add_course: function() {
            // Mutable modification - redraw needed
            this.details.ids.push(-1);
            this.check_options();
            this.do_redraw();
        },
        remove_course: function(index) {
            // Mutable modification - redraw needed
            this.details.ids.splice(index, 1);
            this.check_options();
            this.do_redraw();
        },
        check_options: function() {
            // Check for duplicates
            this.non_unique_options = false;
            var found = [];

            for (var index in this.details.ids) {
                var value = this.details.ids[index];
                if (found.includes(value)) {
                    this.non_unique_options = true;
                    break;
                }
                found.push(value);
            }

            // Ensure Unit Count is valid:
            this.invalid_units = this.details.unit_count <= 0;
            this.invalid_units_step = this.details.unit_count % 6 !== 0;
        },
        // https://michaelnthiessen.com/force-re-render/
        do_redraw: function() {
            this.redraw = true;

            this.$nextTick(() => {
                this.redraw = false;
            });
        }
    },
    template: '#courseRequirementTemplate'
});

// Handler for different Vue components, redirecting to the right component
Vue.component('rule', {
    props: {
        "details": {
            type: Object
        }
    },
    data: function() {
        return {
            component_names: COMPONENT_NAMES
        }
    },
    template: '#requirementTemplate'
});

// Contains a set of rules, with a button to add more
Vue.component('requirement_container', {
    props: {
        "rules": {
            type: Array
        },
        // Message inserted between rules
        "separator": {
            type: String,
            default: ""
        }
    },
    data: function() {
        return {
            show_add_a_rule_modal: false,
            add_a_rule_modal_option: 'course',

            component_names: COMPONENT_NAMES,

            // Forces the element to re-render, if mutable events occurred
            redraw: false
        }
    },
    methods: {
        add_rule: function() {
            this.show_add_a_rule_modal = false;
            this.rules.push({
                type: 'course',
            });
            this.do_redraw();
        },
        remove: function(index) {
            this.rules.splice(index, 1);
            this.do_redraw();
        },
        // https://michaelnthiessen.com/force-re-render/
        do_redraw: function() {
            this.redraw = true;

            this.$nextTick(() => {
                this.redraw = false;
            });
        }
    },
    template: '#ruleContainerTemplate'
});

/**
 * Submits the rules form.
 */
function handleRules() {
    // Serialize list structures - this doesn't translate well over POST requests normally.
    document.getElementById("rules").value = JSON.stringify(app.rules);

    return true;
}

var app = new Vue({
    el: '#requirementsContainer',
    data: {
        rules: []
    }
});

var reqs = document.getElementById("rules").value.trim();
if (reqs.length > 0) {
    var parsed = JSON.parse(reqs);
    if (parsed != null) {
        app.rules = parsed;
    }
}
