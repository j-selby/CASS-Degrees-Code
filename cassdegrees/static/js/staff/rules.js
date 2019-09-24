//! Vue.js based means of adding/removing rules. Excludes serialization (see programmanagement.js)

// Stores a JSON of all rule names, for internal reference only.
const ALL_COMPONENT_NAMES = {
    'incompatibility': "Incompatibility",
    'program': 'Program',
    'subplan': "Subplan",
    'course': "Course",
    'course_list': "Course List",
    'course_requisite': "Course Requisite",
    'custom_text': "Custom (Text)",
    'custom_text_req': "Custom (Text)",
    'elective': "Elective Units",
    'either_or': "Either Or"
};

// Help for all components
const ALL_COMPONENT_HELP = {
    'incompatibility': "A rule which notes that students must not have picked any of the set of courses specified.",
    'program': 'A rule which enforces that only students from a particular course can take this option.',
    'subplan': "A rule which gives students a choice from a particular set of majors, minors, specialisations or " +
               "other subplans. The description here is used to describe the rule when displaying this rule to " +
               "students.",
    'course': "A rule which specifies that students should pick a certain amount of units from a set of available " +
              "courses.",
    'course_requisite': "A rule which specifies that students should have taken a set of courses before taking this " +
                        "one.",
    'custom_text': "If other rules don't entirely fit the requirements of a rule, the custom text field allows " +
                   "for the specification of other program content. Note that this isn't enforced in student-facing " +
                   "tools.",
    'custom_text_req': "If other rules don't entirely fit the requirements of a rule, the custom text field allows " +
                       "for the specification of other program content. Note that this isn't enforced in student-facing " +
                       "tools.",
    'elective': "A rule which allows students to choose any courses offered by the ANU as electives to fill a set" +
                " amount of units.",
    'either_or': "A rule which allows for the specification of sets of different paths that students can take. Each " +
                 "\"OR\" group is a collection of rules which must be completed if students were to pick that specific " +
                 "group."
};

// Translation table between internal names for components and human readable ones.
const COMPONENT_NAMES = {
    'subplan': "Subplan",
    'course_list': "Course List",
    'custom_text': "Custom (Text)",
    'elective': "Elective",
    'either_or': "Either Or"
};

// For either rule, list everything in the drop down menu except the "Either" option, or recursion will occur.
const EITHER_OR_COMPONENT_NAMES = {
    'subplan': "Subplan",
    'course': "Course",
    'custom_text': "Custom (Text)",
    'elective': "Elective"
};

//
const REQUISITE_COMPONENT_NAMES = {
    'incompatibility': "Incompatibility",
    'program': 'Program',
    'elective': "Elective",
    'course_requisite': "Course Requisite",
    'custom_text_req': "Custom (Text)",
    'either_or': "Either Or"
};

const REQUISITE_EITHER_OR_COMPONENT_NAMES = {
    'program': 'Program',
    'elective': "Elective",
    'course_requisite': "Course",
    'custom_text_req': "Custom (Text)"
};

const LIST_TYPES = {
    'min': 'At least',
    'exact': 'Exactly',
    'max': 'No more than'
};

const SUBPLAN_TYPES = {
    'MAJ':  'Majors',
    'MIN':  'Minors',
    'SPEC': 'Specialisations'
};

const INFO_MSGS = {
    'course': '<p>This Requisite requires Courses in the system. Please create Courses ' +
        '<a href="/staff/create/course/" target="_blank">here</a> or bulk upload Courses ' +
        '<a href="/staff/bulk_upload/" target="_blank">here</a> first before creating this Requisite.</p>',
    'subplan': '<p>This Requisite requires Subplans in the system. Please create Subplans ' +
        '<a href="/staff/create/subplan/" target="_blank">here</a> first before creating this Requisite.</p>',
    'program': '<p>This Requisite requires Programs in the system. Please create Programs ' +
        '<a href="/staff/create/program/" target="_blank">here</a> first before creating this Requisite.</p>'
};

// Contains a set of rules, with a button to add more
Vue.component('rule_container', {
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
            add_a_rule_modal_option: 'course_list',

            component_groups: { 'rules': COMPONENT_NAMES, 'requisites': REQUISITE_COMPONENT_NAMES},
            component_names: null,

            // Forces the element to re-render, if mutable events occurred
            redraw: false,
        }
    },
    methods: {
        add_rule: function() {
            this.show_add_a_rule_modal = false;
            this.rules.push({
                type: this.add_a_rule_modal_option,
            });
        },
        remove: function(index) {
            this.rules.splice(index, 1);
        },
        duplicate_rule: function(index) {
            // JSON.parse(JSON.stringify(...)) is done to actually duplicate the contents of the rule, rather than just copying the memory references.
            this.rules.push(JSON.parse(JSON.stringify(this.rules[index])));
        },
        check_options: function() {
            var valid = true;
            for (var index in this.$children){
                valid = valid && this.$children[index].check_options();
            }

            return valid;
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
    var valid = true;
    for (var index in app.$children){
        valid = valid && app.$children[index].check_options();
    }

    // Serialize list structures - this doesn't translate well over POST requests normally.
    document.getElementById("rules").value = JSON.stringify(app.rules);

    return valid;
}

var app = new Vue({
    el: '#rulesContainer',
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


function redrawVueComponents() {
    for (var index in app.$children){
        app.$children[index].do_redraw();
    }
}
