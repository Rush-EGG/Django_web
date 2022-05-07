from django import forms


class BootStrap:
    # 什么样的表单不需要加bootstrap样式，剔除
    bootstrap_exclude_field = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环所有字段，如果原先已有样式，则给他们添加上想要的样式
        # 如果原先样式为空，那么直接硬塞给他
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_field:
                continue
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }


class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass


class BootStrapForm(BootStrap, forms.Form):
    pass
