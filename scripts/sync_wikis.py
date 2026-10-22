#!/usr/bin/env python3

import os
import shutil
import subprocess
import tempfile
import re
from datetime import datetime
import markdown

MODS = [
    {
        'slug': 'claim',
        'name': 'Claim',
        'repo': 'Claim',
        'icon': 'claim.svg',
        'curseforge': 'https://www.curseforge.com/minecraft/mc-mods/claim',
        'modrinth': 'https://modrinth.com/mod/claim',
        'github': 'https://github.com/yigit-guven/Claim'
    },
    {
        'slug': 'day-length',
        'name': 'Day Length',
        'repo': 'Day-Length',
        'icon': 'daylength.svg',
        'curseforge': 'https://www.curseforge.com/minecraft/mc-mods/day-length/',
        'modrinth': 'https://modrinth.com/mod/day-length/',
        'github': 'https://github.com/yigit-guven/Day-Length'
    },
    {
        'slug': 'easy-hammers',
        'name': 'Easy Hammers',
        'repo': 'Easy-Hammers',
        'icon': 'easyhammers.svg',
        'curseforge': 'https://www.curseforge.com/minecraft/mc-mods/easy-hammers',
        'modrinth': 'https://modrinth.com/mod/easy-hammers',
        'github': 'https://github.com/yigit-guven/Easy-Hammers'
    },
    {
        'slug': 'leather-craft',
        'name': 'Leather Craft',
        'repo': 'Leather-Craft',
        'icon': 'leathercraft.svg',
        'curseforge': 'https://www.curseforge.com/minecraft/mc-mods/leather-craft',
        'modrinth': 'https://modrinth.com/mod/leather-craft',
        'github': 'https://github.com/yigit-guven/Leather-Craft'
    },
    {
        'slug': 'petting',
        'name': 'Petting',
        'repo': 'Petting',
        'icon': 'petting.svg',
        'curseforge': 'https://www.curseforge.com/minecraft/mc-mods/petting',
        'modrinth': 'https://modrinth.com/mod/petting',
        'github': 'https://github.com/yigit-guven/Petting'
    },
    {
        'slug': 'rpg-backpacks',
        'name': 'RPG Backpacks',
        'repo': 'RPG-Backpacks',
        'icon': 'backpacks.svg',
        'curseforge': 'https://www.curseforge.com/minecraft/mc-mods/rpg-backpacks',
        'modrinth': 'https://modrinth.com/mod/rpg-backpacks',
        'github': 'https://github.com/yigit-guven/RPG-Backpacks'
    },
    {
        'slug': 'vault-ui',
        'name': 'Vault UI',
        'repo': 'Vault-UI',
        'icon': 'vaultui.svg',
        'curseforge': 'https://www.curseforge.com/minecraft/mc-mods/vault-ui',
        'modrinth': 'https://modrinth.com/mod/vault-ui',
        'github': 'https://github.com/yigit-guven/Vault-UI'
    }
]

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MC_MODS_DIR = os.path.join(BASE_DIR, 'minecraft-mods')
SITEMAP_PATH = os.path.join(BASE_DIR, 'sitemap.xml')
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'wiki_template.html')
WIKI_CSS_PATH = os.path.join(MC_MODS_DIR, 'wiki.css')

with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    WIKI_TEMPLATE = f.read()

with open(WIKI_CSS_PATH, 'r', encoding='utf-8') as f:
    INLINE_WIKI_CSS = f.read()


def convert_markdown(text, mod_slug, root_path):
    if not text:
        return ""

    mod_slug = mod_slug.lower()

    def rewrite_relative_url(url):
        if re.match(r'^(https?:|mailto:|#|//)', url, re.IGNORECASE):
            return url

        anchor = ""
        if '#' in url:
            url_part, anchor = url.split('#', 1)
            anchor = '#' + anchor.lower()
        else:
            url_part = url

        if 'minecraft-mods/' in url_part.lower():
            idx = url_part.lower().find('minecraft-mods/')
            tail = url_part[idx + len('minecraft-mods/'):].strip('/')
            parts = tail.split('/', 1)
            target_mod = parts[0].lower()
            page = parts[1].lower() if len(parts) > 1 else ''
            if page.endswith('.html'):
                page = page[:-5]
            if page == 'home' or page == '':
                return f"{root_path}minecraft-mods/{target_mod}/{anchor}"
            else:
                return f"{root_path}minecraft-mods/{target_mod}/{page}/{anchor}"

        clean = re.sub(r'\.md$', '', url_part, flags=re.IGNORECASE).strip('/')
        if clean.lower().startswith(mod_slug + '/'):
            clean = clean[len(mod_slug) + 1:]

        if clean.lower() == 'home' or clean == '':
            return f"{root_path}minecraft-mods/{mod_slug}/{anchor}"
        else:
            return f"{root_path}minecraft-mods/{mod_slug}/{clean.lower()}/{anchor}"

    def link_replacer(match):
        label = match.group(1)
        url = match.group(2)
        new_url = rewrite_relative_url(url)
        return f"[{label}]({new_url})"

    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_replacer, text)

    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'nl2br'])
    html = md.convert(text)

    html = re.sub(r'(<table\b[^>]*>[\s\S]*?</table>)', r'<div class="wiki-table-container">\1</div>', html)

    def html_href_replacer(match):
        prefix = match.group(1)
        quote = match.group(2)
        url = match.group(3)
        new_url = rewrite_relative_url(url)
        return f'{prefix}{quote}{new_url}{quote}'

    html = re.sub(r'(<a\s+[^>]*href=)(["\'])([^"\']+)\2', html_href_replacer, html)
    return html


def build_sidebar_html(sidebar_md, mod, current_page_slug, root_path):
    mod_slug = mod['slug'].lower()
    page_slug_lower = current_page_slug.lower()

    if sidebar_md:
        cleaned_md = re.sub(r'([^\n])\n\s*([-*]\s+\[)', r'\1\n\n\2', sidebar_md)
        html = convert_markdown(cleaned_md, mod_slug, root_path)
        html = re.sub(r'(?:<br\s*/?>|\n)\s*[-*]\s*(<a\s)', r'<br>\1', html)
        html = re.sub(r'^\s*[-*]\s*(<a\s)', r'\1', html)

        current_href = f"{root_path}minecraft-mods/{mod_slug}/" if page_slug_lower == 'home' else f"{root_path}minecraft-mods/{mod_slug}/{page_slug_lower}/"
        current_href_noslash = current_href.rstrip('/')
        pattern = rf'href=(["\'])({re.escape(current_href)}|{re.escape(current_href_noslash)})\1'
        html = re.sub(pattern, rf'href="{current_href}" class="active"', html)
        return html

    home_active = ' class="active"' if page_slug_lower == 'home' else ''
    return f"""
        <ul>
            <li><a href="{root_path}minecraft-mods/{mod_slug}/"{home_active}>Home</a></li>
        </ul>
    """


def generate_page_html(mod, page_slug, content_html, sidebar_html, root_path, robots_meta='index, follow'):
    mod_slug = mod['slug'].lower()
    page_slug_lower = page_slug.lower()
    is_home = (page_slug_lower == 'home')

    display_title = page_slug.replace('-', ' ')
    page_title = f"{mod['name']} Wiki | Yiğit Güven" if is_home else f"{display_title} | {mod['name']} Wiki | Yiğit Güven"
    page_desc = f"Documentation, guides, and mechanics for {mod['name']} Minecraft mod."
    canonical_url = f"https://yigitguven.net/minecraft-mods/{mod_slug}/" if is_home else f"https://yigitguven.net/minecraft-mods/{mod_slug}/{page_slug_lower}/"
    breadcrumb_label = "Home" if is_home else display_title
    github_edit_page = page_slug

    mod_icon = mod.get('icon', 'claim.svg')
    favicon_path = f"{root_path}images/projecticons/{mod_icon}"

    html = WIKI_TEMPLATE
    html = html.replace('{{PAGE_TITLE}}', page_title)
    html = html.replace('{{PAGE_DESC}}', page_desc)
    html = html.replace('{{CANONICAL_URL}}', canonical_url)
    html = html.replace('{{ROBOTS_META}}', robots_meta)
    html = html.replace('{{FAVICON_PATH}}', favicon_path)
    html = html.replace('{{MOD_SLUG}}', mod_slug)
    html = html.replace('{{MOD_NAME}}', mod['name'])
    html = html.replace('{{BREADCRUMB_LABEL}}', breadcrumb_label)
    html = html.replace('{{GITHUB_REPO_URL}}', mod['github'])
    html = html.replace('{{GITHUB_PAGE}}', github_edit_page)
    html = html.replace('{{SIDEBAR_HTML}}', sidebar_html)
    html = html.replace('{{CONTENT_HTML}}', content_html)
    html = html.replace('{{ROOT_PATH}}', root_path)
    html = html.replace('{{INLINE_WIKI_CSS}}', INLINE_WIKI_CSS)

    return html


def sync_wikis():
    print("Syncing Minecraft mod wikis...")
    all_wiki_pages = []

    for mod in MODS:
        slug = mod['slug'].lower()
        repo = mod['repo']
        name = mod['name']
        print(f"Processing {name} ({slug})...")

        mod_dir = os.path.join(MC_MODS_DIR, slug)

        if os.path.exists(mod_dir):
            shutil.rmtree(mod_dir)
        os.makedirs(mod_dir, exist_ok=True)

        with tempfile.TemporaryDirectory() as tmpdir:
            clone_url = f"https://github.com/yigit-guven/{repo}.wiki.git"
            res = subprocess.run(['git', 'clone', '--depth', '1', clone_url, tmpdir], capture_output=True, text=True)

            if res.returncode != 0:
                print(f"  Failed to clone wiki for {name}: {res.stderr.strip()}")
                continue

            md_files = [f for f in os.listdir(tmpdir) if f.endswith('.md')]

            sidebar_path = os.path.join(tmpdir, '_Sidebar.md')
            sidebar_md = None
            if os.path.exists(sidebar_path):
                with open(sidebar_path, 'r', encoding='utf-8') as f:
                    sidebar_md = f.read()

            for md_file in md_files:
                if md_file.startswith('_'):
                    continue

                page_slug = md_file[:-3]
                page_slug_lower = page_slug.lower()
                with open(os.path.join(tmpdir, md_file), 'r', encoding='utf-8') as f:
                    content_md = f.read()

                if page_slug_lower == 'home':
                    root_path = "../../"
                    content_html = convert_markdown(content_md, slug, root_path)
                    sidebar_html = build_sidebar_html(sidebar_md, mod, page_slug, root_path)
                    page_html = generate_page_html(mod, page_slug, content_html, sidebar_html, root_path)

                    target_file = os.path.join(mod_dir, 'index.html')
                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(page_html)

                    all_wiki_pages.append((slug, 'home'))
                else:
                    root_path_dir = "../../../"
                    content_html_dir = convert_markdown(content_md, slug, root_path_dir)
                    sidebar_html_dir = build_sidebar_html(sidebar_md, mod, page_slug, root_path_dir)
                    page_html_dir = generate_page_html(mod, page_slug, content_html_dir, sidebar_html_dir, root_path_dir)

                    subpage_dir = os.path.join(mod_dir, page_slug_lower)
                    os.makedirs(subpage_dir, exist_ok=True)
                    with open(os.path.join(subpage_dir, 'index.html'), 'w', encoding='utf-8') as sf:
                        sf.write(page_html_dir)

                    root_path_file = "../../"
                    content_html_file = convert_markdown(content_md, slug, root_path_file)
                    sidebar_html_file = build_sidebar_html(sidebar_md, mod, page_slug, root_path_file)
                    page_html_file = generate_page_html(mod, page_slug, content_html_file, sidebar_html_file, root_path_file, robots_meta='noindex, follow')

                    target_file = os.path.join(mod_dir, f"{page_slug_lower}.html")
                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(page_html_file)

                    all_wiki_pages.append((slug, page_slug_lower))

    update_sitemap(all_wiki_pages)
    print("Wiki sync complete.")


def update_sitemap(wiki_pages):
    if not os.path.exists(SITEMAP_PATH):
        return

    today = datetime.now().strftime('%Y-%m-%d')
    with open(SITEMAP_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    marker = "<!-- Minecraft Mods Hub & Wikis Section -->"
    if marker in content:
        base_part = content.split(marker)[0].strip()
    elif "<!-- Minecraft Mods Hub Section -->" in content:
        base_part = content.split("<!-- Minecraft Mods Hub Section -->")[0].strip()
    else:
        base_part = content.split("</urlset>")[0].strip()

    wiki_urls = [
        f"  {marker}",
        f"  <url>\n    <loc>https://yigitguven.net/minecraft-mods/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>"
    ]

    for mod in MODS:
        slug = mod['slug'].lower()
        wiki_urls.append(
            f"  <url>\n    <loc>https://yigitguven.net/minecraft-mods/{slug}/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>"
        )

    for slug, page in sorted(wiki_pages):
        if page.lower() != 'home':
            wiki_urls.append(
                f"  <url>\n    <loc>https://yigitguven.net/minecraft-mods/{slug}/{page}/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.7</priority>\n  </url>"
            )

    new_sitemap = base_part + "\n" + "\n".join(wiki_urls) + "\n</urlset>\n"
    with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(new_sitemap)


if __name__ == '__main__':
    sync_wikis()
