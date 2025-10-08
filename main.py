from reactpy import component, html, hooks, run

# ---- Styles ----
def styles():
    return {
        "container": {
            "maxWidth": "500px",
            "margin": "2rem auto",
            "padding": "1.5rem",
            "borderRadius": "10px",
            "boxShadow": "0 4px 12px rgba(0,0,0,0.1)",
            "backgroundColor": "#f9fafb",
            "fontFamily": "sans-serif",
        },
        "header": {"textAlign": "center", "color": "#111827"},
        "input_group": {
            "display": "flex",
            "gap": "0.5rem",
            "marginBottom": "1rem",
        },
        "input": {
            "flex": "1",
            "padding": "0.5rem 0.75rem",
            "border": "1px solid #d1d5db",
            "borderRadius": "6px",
        },
        "select": {
            "padding": "0.5rem",
            "borderRadius": "6px",
            "border": "1px solid #d1d5db",
        },
        "button": {
            "padding": "0.5rem 0.75rem",
            "border": "none",
            "borderRadius": "6px",
            "backgroundColor": "#2563eb",
            "color": "white",
            "cursor": "pointer",
        },
        "task_item": {
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
            "padding": "0.5rem 0.75rem",
            "borderBottom": "1px solid #e5e7eb",
        },
        "completed": {"textDecoration": "line-through", "color": "#9ca3af"},
        "filter_bar": {
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
            "marginBottom": "1rem",
        },
    }


# ---- Helper ----
def handle_filter_change(e, set_filter_priority):
    val = e["target"]["value"]
    if val == "":
        set_filter_priority(None)
    else:
        set_filter_priority(int(val))


# ---- Task Item ----
@component
def TaskItem(task, on_toggle, on_delete):
    style = styles()
    text_style = style["completed"] if task["completed"] else {}
    return html.li(
        {"style": style["task_item"]},
        html.span(
            {
                "style": text_style,
                "onClick": lambda e: on_toggle(task["id"]),
                "role": "button",
            },
            f"{task['text']} (Priority {task['priority']})",
        ),
        html.button(
            {
                "style": {**style["button"], "backgroundColor": "#dc2626"},
                "onClick": lambda e: on_delete(task["id"]),
            },
            "✕",
        ),
    )


# ---- Main Todo List ----
@component
def TodoList():
    style = styles()

    tasks, set_tasks = hooks.use_state([
        {"id": 0, "text": "Make breakfast", "priority": 0, "completed": False},
        {"id": 1, "text": "Feed the dog", "priority": 0, "completed": False},
        {"id": 2, "text": "Do laundry", "priority": 2, "completed": False},
    ])
    new_task_text, set_new_task_text = hooks.use_state("")
    new_priority, set_new_priority = hooks.use_state(1)
    filter_priority, set_filter_priority = hooks.use_state(None)
    sort_by_priority, set_sort_by_priority = hooks.use_state(False)

    def add_task(_):
        if not new_task_text.strip():
            return
        new_task = {
            "id": len(tasks),
            "text": new_task_text.strip(),
            "priority": int(new_priority),
            "completed": False,
        }
        set_tasks(tasks + [new_task])
        set_new_task_text("")

    def toggle_task(task_id):
        set_tasks([
            {**t, "completed": not t["completed"]} if t["id"] == task_id else t
            for t in tasks
        ])

    def delete_task(task_id):
        set_tasks([t for t in tasks if t["id"] != task_id])

    # Apply filters and sorting
    filtered = tasks
    if filter_priority is not None:
        filtered = [t for t in filtered if t["priority"] <= int(filter_priority)]
    if sort_by_priority:
        filtered = sorted(filtered, key=lambda t: t["priority"])

    return html.section(
        {"style": style["container"]},
        html.h1({"style": style["header"]}, "🌟 My Todo List"),

        # Input Row
        html.div(
            {"style": style["input_group"]},
            html.input({
                "style": style["input"],
                "placeholder": "Add new task...",
                "value": new_task_text,
                "onChange": lambda e: set_new_task_text(e["target"]["value"]),
            }),
            html.select(
                {
                    "style": style["select"],
                    "value": str(new_priority),
                    "onChange": lambda e: set_new_priority(int(e["target"]["value"])),
                },
                html.option({"value": "0"}, "Low"),
                html.option({"value": "1"}, "Medium"),
                html.option({"value": "2"}, "High"),
            ),
            html.button({"style": style["button"], "onClick": add_task}, "Add"),
        ),

        # Filter Bar
        html.div(
            {"style": style["filter_bar"]},
            html.label(
                "Filter by priority: ",
                html.select(
                    {
                        "style": style["select"],
                        "onChange": lambda e: handle_filter_change(
                            e, set_filter_priority
                        ),
                    },
                    html.option({"value": ""}, "All"),
                    html.option({"value": "0"}, "Low"),
                    html.option({"value": "1"}, "Medium"),
                    html.option({"value": "2"}, "High"),
                ),
            ),
            html.label(
                html.input({
                    "type": "checkbox",
                    "checked": sort_by_priority,
                    "onChange": lambda e: set_sort_by_priority(not sort_by_priority),
                }),
                " Sort by priority",
            ),
        ),

        # Task List
        html.ul([TaskItem(task, toggle_task, delete_task) for task in filtered]),
    )


# ---- Run App ----
run(TodoList)
