import re

def update_ui_portraits():
    with open('dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add PERSON_AVATARS constant before renderCanvasTree or near GENEALOGY_DATA
    avatars_definition = """
const PERSON_AVATARS = {
  "P-0008": { src: "photos/portrait-agripina-belova-oval.jpg", title: "Подлинная фотография 1960-х гг.", badge: "📷", type: "photo" },
  "P-0014": { src: "photos/portrait-p0014-aleksandr-belov.jpg", title: "Историческая реконструкция: крестьянин Поволжья конца XIX в.", badge: "🎨", type: "reconstruction" },
  "P-0030": { src: "photos/portrait-p0030-fedor-belov.jpg", title: "Историческая реконструкция: дело НКВД 1935 г.", badge: "🎨", type: "reconstruction" },
  "P-0031": { src: "photos/portrait-p0031-pavel-belov.jpg", title: "Историческая реконструкция: гв. сержант ВОВ 1945 г.", badge: "🎨", type: "reconstruction" },
  "P-0032": { src: "photos/portrait-p0032-ivan-belov.jpg", title: "Историческая реконструкция: рядовой 1169 сп 1943 г., орден Красной Звезды", badge: "🎨", type: "reconstruction" },
  "P-0036": { src: "photos/portrait-p0036-vladimir-belov.jpg", title: "Историческая реконструкция: ст. техник-лейтенант РККА", badge: "🎨", type: "reconstruction" }
};
"""

    if 'const PERSON_AVATARS =' not in content:
        content = content.replace('const CANVAS_MARRIAGES = [', avatars_definition + '\nconst CANVAS_MARRIAGES = [')
        print("Added PERSON_AVATARS definition")

    # 2. Update avatarHtml generation in renderCanvasTree
    old_avatar_block = """      let avatarHtml = "";
      if (p.id === "P-0008") {
        avatarHtml = `
          <img class="card-avatar-img" src="photos/portrait-agripina-belova-oval.jpg" alt="${p.name}">
          <div class="card-avatar-badge" title="Подлинная фотография 1960-х гг.">📷</div>
        `;
      } else if (p.id === "P-0005") {"""

    new_avatar_block = """      let avatarHtml = "";
      if (PERSON_AVATARS[p.id]) {
        const av = PERSON_AVATARS[p.id];
        avatarHtml = `
          <img class="card-avatar-img" src="${av.src}" alt="${p.name}">
          <div class="card-avatar-badge" title="${av.title}">${av.badge}</div>
        `;
      } else if (p.id === "P-0005") {"""

    if old_avatar_block in content:
        content = content.replace(old_avatar_block, new_avatar_block)
        print("Updated renderCanvasTree avatarHtml")
    else:
        print("WARNING: old_avatar_block not found in renderCanvasTree")

    # 3. Update selectPerson header in inspector
    old_insp_header = """    <div class="insp-header">
      <div class="insp-eyebrow">${p.id} · ${p.genRoman} · ${p.role}</div>
      <h3 class="insp-title">${p.name}</h3>
      <span class="badge ${p.badgeClass}">${humanStatus}</span>
    </div>"""

    new_insp_header = """    <div class="insp-header">
      ${PERSON_AVATARS[p.id] ? `
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:12px;">
          <div style="position:relative;width:76px;height:76px;border-radius:50%;overflow:hidden;border:2.5px solid var(--accent-seal);box-shadow:0 3px 10px rgba(0,0,0,0.25);flex-shrink:0;">
            <img src="${PERSON_AVATARS[p.id].src}" alt="${p.name}" style="width:100%;height:100%;object-fit:cover;">
            <div style="position:absolute;bottom:0;right:0;background:var(--accent-seal);color:#fff;font-size:11px;padding:2px 5px;border-radius:4px;" title="${PERSON_AVATARS[p.id].title}">${PERSON_AVATARS[p.id].badge}</div>
          </div>
          <div>
            <div class="insp-eyebrow">${p.id} · ${p.genRoman} · ${p.role}</div>
            <h3 class="insp-title" style="margin:2px 0 4px;">${p.name}</h3>
            <div style="font-size:11px;color:var(--ink-500);margin-bottom:4px;">${PERSON_AVATARS[p.id].title}</div>
            <span class="badge ${p.badgeClass}">${humanStatus}</span>
          </div>
        </div>
      ` : `
        <div class="insp-eyebrow">${p.id} · ${p.genRoman} · ${p.role}</div>
        <h3 class="insp-title">${p.name}</h3>
        <span class="badge ${p.badgeClass}">${humanStatus}</span>
      `}
    </div>"""

    if old_insp_header in content:
        content = content.replace(old_insp_header, new_insp_header)
        print("Updated inspector header with portrait")
    else:
        print("WARNING: old_insp_header not found in selectPerson")

    # 4. Update map relatives avatar
    old_map_rel = """    const isAgripina = p.id === "P-0008";
    const avatarInner = isAgripina
      ? `<img src="photos/portrait-agripina-belova-oval.jpg" alt="${p.name}">`
      : `<span>${p.name[0]}</span>`;"""

    new_map_rel = """    const hasAvatar = !!PERSON_AVATARS[p.id];
    const avatarInner = hasAvatar
      ? `<img src="${PERSON_AVATARS[p.id].src}" alt="${p.name}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">`
      : `<span>${p.name[0]}</span>`;"""

    if old_map_rel in content:
        content = content.replace(old_map_rel, new_map_rel)
        print("Updated map dossier avatar logic")

    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("dashboard.html and index.html synchronized with portraits")

if __name__ == '__main__':
    update_ui_portraits()
