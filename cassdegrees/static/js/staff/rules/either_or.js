Vue.component('rule_either_or', {
    props: {
        "details": {
            type: Object,
            validator: function (value) {
                // Ensure that the object has all the attributes we need
                if (!value.hasOwnProperty("either_or")) {
                    value.either_or = [];
                }

                return true;
            }
        },
        // Message inserted between rules
        "separator": {
            type: String,
            default: ""
        },
        // Refresh is used to redraw the sub rules without nuking everything.
        // The prop is bound when the either_or is defined, and upon updating
        // a prop, the rules will be updated without deleting them first.
        "refresh": {
            type: Array,
        }
    },
    data: function() {
        return {
            show_add_a_rule_modal: false,
            which_or: 0,
            add_a_rule_modal_option: 'course_list',

            // Show warnings if appropriate
            large_unit_count: false,

            component_groups: { 'rules': EITHER_OR_COMPONENT_NAMES, 'requisites': REQUISITE_EITHER_OR_COMPONENT_NAMES},
            component_names: EITHER_OR_COMPONENT_NAMES,

            is_eitheror: true,
        }
    },
    methods: {
        add_or: function() {
            this.details.either_or.push([]);
            this.do_redraw();
        },
        add_rule: function() {
            this.show_add_a_rule_modal = false;
            // Add chosen rule to the right or group (based on the button clicked).
            this.details.either_or[this.which_or].push({
                type: this.add_a_rule_modal_option,
            });
        },
        remove: function(index, group) {
            console.log(this.details.either_or[group]);
            this.details.either_or[group].splice(index, 1);
            this.count_units();
            this.do_redraw();
        },
        duplicate_rule: function(index, group) {
            // JSON.parse(JSON.stringify(...)) is done to actually duplicate the contents of the rule, rather than just copying the memory references.
            this.details.either_or[group].push(JSON.parse(JSON.stringify(this.details.either_or[group][index])));
            this.do_redraw();
        },
        remove_group: function(group) {
            this.details.either_or.splice(group, 1);
            this.count_units();
            this.do_redraw();
        },
        duplicate_group: function(group) {
            // JSON.parse(JSON.stringify(...)) is done to actually duplicate the contents of the rule, rather than just copying the memory references.
            this.details.either_or.splice(group, 0, JSON.parse(JSON.stringify(this.details.either_or[group])));
            this.do_redraw();
        },
        check_options: function() {
            var valid = true;
            for (var index in this.$children){
                valid = valid && this.$children[index].check_options();
            }

            return valid;
        },
        count_units: function() {
            // Will go through each rule and determine how many units it specifies, showing a warning if over 48
            for(var or_group of this.details.either_or){
                var units = 0;
                for(var rule of or_group) {
                    if (rule.hasOwnProperty("subplan_type")) {
                        switch (rule.subplan_type) {
                            case "MAJ" : units += 48; break;
                            case "MIN" : units += 24; break;
                            case "SPEC": units += 24; break;
                        }
                    }
                    else if (rule.hasOwnProperty("unit_count")) {
                        units += parseInt(rule.unit_count);
                    }
                }

                if (units > 48) {
                    this.large_unit_count = true;
                    return;
                }
            }
            this.large_unit_count = false;
        },
        // https://michaelnthiessen.com/force-re-render/
        do_redraw: function() {
            this.refresh.push("");
        }
    },
    template: '#eitherOrTemplate'
});
