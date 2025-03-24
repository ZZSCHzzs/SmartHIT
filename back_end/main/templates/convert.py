import os
import re


def django_to_vue(django_template_content):
    """
    将Django模板文件内容转换为Vue组件内容
    """
    # 移除外部JS和CSS引入

    vue_template_content = re.sub(r'<link.*?rel="stylesheet".*?>', '', django_template_content, flags=re.DOTALL)
    vue_template_content = re.sub(r'<script.*?src=".*?".*?></script>', '', vue_template_content, flags=re.DOTALL)

    # 替换变量表达式：{{ variable }} -> {{ variable }}
    vue_template_content = re.sub(r'{{\s*(.*?)\s*}}', r'{{ \1 }}', vue_template_content)

    # 替换模板标签：{% if condition %} -> v-if="condition"
    vue_template_content = re.sub(r'{%\s*if\s+(.*?)\s*%}', r'<div v-if="\1">', vue_template_content)

    # 替换 else {% else %} -> </div><div v-else>
    vue_template_content = vue_template_content.replace('{% else %}', '</div><div v-else>')

    # 替换 endif {% endif %} -> </div>
    vue_template_content = vue_template_content.replace('{% endif %}', '</div>')

    # 替换for循环：{% for item in items %} -> <div v-if="items.length > 0"><div v-for="item in items" :key="item.id">
    vue_template_content = re.sub(
        r'{%\s*for\s+(\w+)\s+in\s+([\w.]+)\s*%}',
        r'<div v-if="\2.length > 0"><div v-for="\1 in \2" :key="\1.id">',
        vue_template_content
    )
    vue_template_content = vue_template_content.replace('{% endfor %}', '</div></div>')

    # 处理 {% empty %}：将其替换为 <template v-else>
    vue_template_content = vue_template_content.replace('{% empty %}', '</div></div><div v-else>')

    # 替换block和endblock（这些可以根据实际需求进行调整）
    vue_template_content = re.sub('{% block .*? %}', '', vue_template_content)
    vue_template_content = vue_template_content.replace('{% endblock %}', '')

    # 替换 {% load static %}、{% csrf_token %} 和 {% extends %}
    vue_template_content = vue_template_content.replace('{% load static %}', '')
    vue_template_content = vue_template_content.replace('{% csrf_token %}', '')
    vue_template_content = re.sub(r'{% extends .*? %}', '', vue_template_content)

    vue_template_content = vue_template_content.replace('==', '===')
    vue_template_content = vue_template_content.replace(' or ', ' || ')
    # 替换带有查询参数的 <a> 标签为 <router-link>
    vue_template_content = re.sub(
        r'<a\s+href="(/[^?]+)?\?(\w+)=\{\{\s*(.*?)\s*\}\}"\s*([^>]*)>(.*?)</a>',
        r'<router-link :to="{ path: `\1`, query: { \2: \3 } }" \4>\5</router-link>',
        vue_template_content
    )

    # 替换带有动态路径参数的 <a> 标签为 <router-link>
    vue_template_content = re.sub(
        r'<a\s+href="(/[^"]*?){{\s*(.*?)\s*}}"\s*([^>]*)>(.*?)</a>',
        r'<router-link :to="{ path: `\1${\2}` }" \3>\4</router-link>',
        vue_template_content
    )

    # 替换静态的 <a> 标签为 <router-link>
    vue_template_content = re.sub(
        r'<a\s+href="(/[^"]*)"\s*([^>]*)>(.*?)</a>',
        r'<router-link :to="{ path: `\1` }" \2>\3</router-link>',
        vue_template_content
    )

    # 替换 {% static 'path' %} 静态资源路径
    vue_template_content = re.sub(
        r'{%\s*static\s+\'(.*?)\'\s*%}',
        r'/\1',
        vue_template_content
    )

    # 替换 {% static 'path'|add:variable %} 静态资源路径
    vue_template_content = re.sub(
        r'{%\s*static\s+\'(.*?)\'\|add:(.*?)\s*%}',
        r'/\1${\2}',
        vue_template_content
    )

    # 替换 |date:"Y.m.d" 过滤器为 Vue 的日期格式化方法
    vue_template_content = re.sub(
        r'{{\s*(.*?)\s*\|date:"Y\.m\.d"\s*}}',
        r'{{ $formatDate(\1) }}',
        vue_template_content
    )

    # 替换 |date:"Y.m.d H:i" 过滤器为 Vue 的日期时间格式化方法
    vue_template_content = re.sub(
        r'{{\s*(.*?)\s*\|date:"Y-m-d H:i"\s*}}',
        r'{{ $formatDateTime(\1) }}',
        vue_template_content
    )

    # 替换 |truncatechars 过滤器为 Vue 的截取方法
    vue_template_content = re.sub(
        r'{{\s*(.*?)\s*\|truncatechars:(\d+)\s*}}',
        r'{{ $truncate(\1, \2) }}',
        vue_template_content
    )

    # 添加 alt="" 到没有 alt 属性的 <img> 标签
    vue_template_content = re.sub(
        r'(<img\s+((?!alt=)[^>])*?)\s*(\/?)>',
        r'\1 alt="" \3>',
        vue_template_content
    )

    return vue_template_content


def extract_and_remove_js_css(django_template_content):
    """
    提取并移除模板中的自定义JS和CSS代码
    """
    django_template_content = re.sub(r'{#(.*?)#}', '', django_template_content)
    custom_js = ''
    custom_css = ''

    # 提取并移除自定义JS代码
    script_match = re.search(r'<script>(.*?)</script>', django_template_content, re.DOTALL)
    if (script_match):
        custom_js = script_match.group(1).strip()
        django_template_content = django_template_content.replace(script_match.group(0), '')

    # 提取并移除自定义CSS代码
    style_match = re.search(r'<style>(.*?)</style>', django_template_content, re.DOTALL)
    if (style_match):
        custom_css = style_match.group(1).strip()
        django_template_content = django_template_content.replace(style_match.group(0), '')

    return custom_js, custom_css, django_template_content


def convert_django_templates_to_vue(input_dir, output_dir):
    """
    将指定目录下的所有Django模板文件转换为Vue组件文件
    """
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    django_template_content = f.read()

                # 提取并移除自定义JS和CSS代码
                custom_js, custom_css, django_template_content = extract_and_remove_js_css(django_template_content)

                vue_template_content = django_to_vue(django_template_content)

                # 计算目标文件路径
                relative_path = os.path.relpath(file_path, input_dir)
                vue_file_path = os.path.join(output_dir, os.path.splitext(relative_path)[0] + '.vue')
                os.makedirs(os.path.dirname(vue_file_path), exist_ok=True)

                # 写入Vue组件文件
                with open(vue_file_path, 'w', encoding='utf-8') as f:
                    f.write(f'<template>\n{vue_template_content}\n</template>\n')
                    f.write('<script>\n')
                    f.write('export default {\n')
                    f.write('  name: \'' + os.path.splitext(file)[0] + '\',\n')
                    if custom_js:
                        f.write('  mounted() {\n')
                        f.write(f'    {custom_js}\n')
                        f.write('  },\n')
                    f.write('};\n')
                    f.write('</script>\n')
                    f.write('<style scoped>\n')
                    if custom_css:
                        f.write(f'{custom_css}\n')
                    f.write('</style>\n')


if __name__ == "__main__":
    input_directory = 'H:/djangoproject/main/templates/'  # 替换为你的Django模板文件夹路径
    output_directory = 'H:/SmartHIT-vue/SmartHIT/src/views/convert'  # 替换为你的Vue组件文件夹路径
    convert_django_templates_to_vue(input_directory, output_directory)
