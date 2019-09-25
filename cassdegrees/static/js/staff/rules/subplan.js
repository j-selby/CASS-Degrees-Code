Vue.component('rule_subplan', {
    props: {
        "details": {
            type: Object,

            validator(value) {
                // Ensure that the object has all the attributes we need
                if (!value.hasOwnProperty("ids")) {
                    value.ids = [-1];
                }

                if (!value.hasOwnProperty("kind")) {
                    value.kind = "";
                }

                if (!value.hasOwnProperty("subplan_type")) {
                    value.subplan_type = "";
                }

                return true;
            }
        }
    },
    data() {
        return {
            "subplans": [],
            "filtered_subplans": [],
            "program_year": "",
            "subplan_types": [],
            "info_msg": INFO_MSGS['subplan'],
            "show_help": false,

            // Display related warnings if true
            "non_unique_options": false,
            "inconsistent_units": false,
            "wrong_year_selected": false,
            "is_blank": false,

            "redraw": false
        }
    },
    created() {
        // Javascript has the best indirection...
        const rule = this;

        const request = new XMLHttpRequest();

        request.addEventListener("load", function () {
            rule.subplans = JSON.parse(request.response);

            rule.check_options();
            rule.apply_subplan_filter();
        });
        request.open("GET", "/api/search/?select=id,code,name,units,year,publish,planType&from=subplan&publish=true");
        request.send();

        rule.subplan_types = SUBPLAN_TYPES;

        // Sets the program year to be the value of the id_year field in the original component
        rule.program_year = document.getElementById('id_year').value;

        // Modifies the original 'id_year' element by telling it to refresh all components on all keystrokes
        document.getElementById('id_year').addEventListener("input", function () {
            app.redraw();
        });

        // Keep a copy of the OR Rule's "count_units" function (Or a blank function if unavailable)
        this.parent_count_units_fn = this.$parent.get_or_rule_count_units_fn();
    },
    methods: {
        apply_subplan_filter() {
            // Create a new array containing the filtered items for vue to read off
            const rule = this;

            if (this.program_year && this.details.subplan_type) {
                this.filtered_subplans = this.subplans.filter(
                    function (item) {
                        return item.planType === rule.details.subplan_type && parseInt(rule.program_year) === item.year;
                    }
                );
            } else
                this.filtered_subplans = [];
        },
        change_filter() {
            // Clear the current list and re-apply the filter
            for (const i in this.details.ids)
                this.details.ids[i] = -1;
            this.apply_subplan_filter();
            this.update_units();
            this.do_redraw();
        },
        add_subplan() {
            // Mutable modification - redraw needed
            this.details.ids.push(-1);
            this.check_options();
            this.do_redraw();
        },
        remove_subplan(index) {
            // Mutable modification - redraw needed
            this.details.ids.splice(index, 1);
            this.check_options();
            this.do_redraw();
        },
        check_options() {
            // Ensure all data has been filled in
            this.is_blank = this.details.kind === "";
            for (const index in this.details.ids) {
                const value = this.details.ids[index];
                if (value === -1 || value === "") {
                    this.is_blank = true;
                    break;
                }
            }

            // Check if invalid subplan year
            this.wrong_year_selected = false;
            year_check:
                for (const selected_index in this.details.ids) {
                    selected_value = this.details.ids[selected_index];
                    for (const element_index in this.subplans) {
                        const element_value = this.subplans[element_index];
                        if (element_value.id == selected_value) {
                            if ("" + element_value['year'] != this.program_year) {
                                this.wrong_year_selected = true;
                                break year_check;
                            }
                        }
                    }
                }

            // Check for duplicates
            this.non_unique_options = false;
            var found = [];

            for (const index in this.details.ids) {
                const value = this.details.ids[index];
                if (found.includes(value)) {
                    this.non_unique_options = true;
                    break;
                }
                found.push(value);
            }

            // Check for inconsistent units
            this.inconsistent_units = false;
            let desired_unit_value = 0;

            for (const index in this.details.ids) {
                const value = this.details.ids[index];
                // Find the raw data for this ID
                for (const element_index in this.subplans) {
                    const element_value = this.subplans[element_index];
                    if (element_value.id === value) {
                        if (desired_unit_value === 0) {
                            desired_unit_value = element_value.units;
                        } else if (desired_unit_value !== element_value.units) {
                            this.inconsistent_units = true;
                        }

                        break;
                    }
                }
            }

            return !this.wrong_year_selected && !this.non_unique_options && !this.inconsistent_units && !this.is_blank;
        },
        update_units() {
            // To be called whenever the unit count is updated. Will ask the OR rule to re-evaluate the unit count
            this.parent_count_units_fn();
            this.check_options();
        },
        // https://michaelnthiessen.com/force-re-render/
        do_redraw() {
            this.program_year = document.getElementById('id_year').value;
            this.redraw = true;

            this.$nextTick(() => {
                this.redraw = false;
            });
        }
    },
    template: '#subplanRuleTemplate'
});
