import React from "react";
import {
  NavLink,
  Navigate,
  Route,
  Routes,
  Link,
  useLocation,
  useParams,
} from "react-router-dom";
import {
  categoryIcons,
  categorySlugs,
  categorySummaries,
  getRelatedSkills,
  getSkill,
  mapColumns,
  skills,
} from "./data/skills.js";

function App() {
  return (
    <>
      <div className="background-grid" aria-hidden="true" />
      <Shell>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/skills" element={<SkillsPage />} />
          <Route path="/skills/:slug" element={<SkillPage />} />
          <Route path="/categorias" element={<CategoriesPage />} />
          <Route path="/categorias/:slug" element={<CategoryPage />} />
          <Route path="/mapa" element={<MapPage />} />
          <Route path="/framework" element={<FrameworkPage />} />
          <Route path="/repos" element={<ReposPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Shell>
    </>
  );
}

function Shell({ children }) {
  const location = useLocation();

  React.useEffect(() => {
    window.scrollTo({ top: 0, behavior: "instant" });
  }, [location.pathname]);

  return (
    <>
      <header className="topbar">
        <Link className="brand" to="/">
          <span className="brand-mark" aria-hidden="true">
            <img alt="" src="./assets/argentina-flag.svg" />
          </span>
          <span className="brand-text">
            <strong>AR Skills Ecosystem</strong>
            <small>Legal + Tech + Bureaucracy Flows</small>
          </span>
        </Link>
        <nav className="main-nav" aria-label="Secciones principales">
          <NavLink to="/skills">Skills</NavLink>
          <NavLink to="/categorias">Categorias</NavLink>
          <NavLink to="/mapa">Mapa</NavLink>
          <NavLink to="/framework">Framework</NavLink>
          <NavLink to="/repos">Repos</NavLink>
        </nav>
      </header>
      <main className="site-main">{children}</main>
    </>
  );
}

function HomePage() {
  return (
    <>
      <section className="hero section">
        <div className="hero-copy">
          <p className="eyebrow">Ecosistema de skills para Argentina</p>
          <h1>Procesos complejos, legales y burocraticos convertidos en flujos guiados.</h1>
          <p className="hero-text">
            Un hub para navegar skills orientadas a propiedad intelectual, contratos,
            compliance, fiscalidad, comercio exterior y validacion documental para software
            y operaciones digitales en Argentina.
          </p>
          <div className="hero-actions">
            <Link className="button primary" to="/skills">
              Explorar Skills
            </Link>
            <Link className="button ghost" to="/mapa">
              Ver Mapa
            </Link>
          </div>
          <p className="hero-subline">
            Repos independientes, una sola narrativa visual y una arquitectura común para automatizar
            fricción legal-operativa.
          </p>
          <div className="hero-metrics">
            <Metric value={skills.length} label="skills activas" />
            <Metric value={Object.keys(categorySummaries).length} label="categorias" />
            <Metric value={new Set(skills.map((skill) => skill.agency)).size} label="organismos / marcos" />
          </div>
        </div>
        <aside className="hero-stage">
          <FeaturedCarousel items={skills.slice(0, 4)} />
        </aside>
      </section>

      <section className="section">
        <SectionHeading
          eyebrow="Clusters"
          title="La coleccion funciona como sistema"
          copy="No es una lista plana. Cada grupo resuelve un area distinta y algunas skills alimentan a otras."
        />
        <div className="category-grid">
          {Object.entries(categorySummaries).map(([name, summary]) => (
            <article className="category-card" key={name}>
              <div className="category-card-topline">
                <span className="category-icon">{categoryIcons[name]}</span>
                <span className="panel-label">{skills.filter((skill) => skill.category === name).length} skills</span>
              </div>
              <h3>{name}</h3>
              <p>{summary}</p>
              <div className="tag-strip">
                {skills
                  .filter((skill) => skill.category === name)
                  .slice(0, 4)
                  .map((skill) => (
                    <span className="tag" key={skill.slug}>
                      {skill.name}
                    </span>
                  ))}
              </div>
              <div className="card-actions">
                <Link className="mini-link" to={`/categorias/${categorySlugs[name]}`}>
                  Ver categoría
                </Link>
                {skills
                  .filter((skill) => skill.category === name)
                  .slice(0, 2)
                  .map((skill) => (
                    <a className="mini-link subtle" href={skill.repo} key={skill.slug} target="_blank" rel="noreferrer">
                      {skill.name}
                    </a>
                  ))}
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="section">
        <SectionHeading
          eyebrow="Entradas"
          title="Rutas reales por skill"
          copy="Cada skill tiene su propia URL dentro del hub y link directo a su repo en GitHub. Eso permite compartir piezas puntuales sin perder la lectura sistémica."
        />
        <div className="skills-ribbon">
          {skills.map((skill) => (
            <article className={`ribbon-card tone-${skill.color}`} key={skill.slug}>
              <Link className="ribbon-card-link" to={`/skills/${skill.slug}`}>
                <span className="ribbon-icon">{skill.icon}</span>
                <small>{skill.agency}</small>
                <strong>{skill.name}</strong>
                <span>{skill.version}</span>
              </Link>
              <a className="mini-link" href={skill.repo} target="_blank" rel="noreferrer">
                GitHub
              </a>
            </article>
          ))}
        </div>
      </section>

      <section className="section">
        <SectionHeading
          eyebrow="Pathways"
          title="Flujos que se leen como producto"
          copy="La v2 visual no muestra solo repos: muestra recorridos posibles dentro del ecosistema."
        />
        <div className="pathways-grid">
          <PathwayCard
            title="Producto digital"
            steps={["Terms + Privacy", "Personal Data Registry", "Legal Documentation Validation"]}
            tone="teal"
          />
          <PathwayCard
            title="Cierre comercial"
            steps={["Software Development Contract", "NDA", "Service Export Invoicing"]}
            tone="rose"
          />
          <PathwayCard
            title="Proteccion e expansion"
            steps={["Trademark Registration", "Software Copyright Registration", "Knowledge Economy Law"]}
            tone="brand"
          />
        </div>
      </section>
    </>
  );
}

function SkillsPage() {
  const [search, setSearch] = React.useState("");
  const [category, setCategory] = React.useState("Todas");
  const [agency, setAgency] = React.useState("Todos");

  const categories = React.useMemo(() => ["Todas", ...new Set(skills.map((skill) => skill.category))], []);
  const agencies = React.useMemo(() => ["Todos", ...new Set(skills.map((skill) => skill.agency))], []);

  const list = skills.filter((skill) => {
    const matchesCategory = category === "Todas" || skill.category === category;
    const matchesAgency = agency === "Todos" || skill.agency === agency;
    const haystack = [
      skill.name,
      skill.tagline,
      skill.category,
      skill.agency,
      skill.law,
      ...skill.tags,
      ...skill.outputs,
    ]
      .join(" ")
      .toLowerCase();
    return matchesCategory && matchesAgency && haystack.includes(search.toLowerCase());
  });

  return (
    <section className="section">
      <SectionHeading
        eyebrow="Explorer"
        title="Catalogo con filtros"
        copy="Ahora la navegacion principal vive en una vista de exploracion con filtros persistentes y links reales a cada skill."
      />
      <div className="explorer-layout">
        <aside className="control-panel">
          <label className="search-box">
            <span>Buscar</span>
            <input
              type="search"
              placeholder="Marca, AAIP, contrato, INPI..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </label>
          <FilterGroup title="Categoria" options={categories} value={category} onChange={setCategory} />
          <FilterGroup title="Organismo" options={agencies} value={agency} onChange={setAgency} />
        </aside>
        <div className="explorer-results">
          <div className="explorer-toolbar">
            <span>{list.length} skills visibles</span>
            <div className="active-filters">
              {category !== "Todas" ? <span className="tag">{category}</span> : null}
              {agency !== "Todos" ? <span className="tag">{agency}</span> : null}
              {search ? <span className="tag">buscar: {search}</span> : null}
            </div>
          </div>
          <div className="skills-grid">
            {list.map((skill) => (
              <SkillCard key={skill.slug} skill={skill} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function SkillPage() {
  const { slug } = useParams();
  const skill = getSkill(slug);

  if (!skill) {
    return <Navigate to="/skills" replace />;
  }

  const related = getRelatedSkills(skill);

  return (
    <>
      <section className={`skill-hero tone-${skill.color}`}>
        <div className="skill-hero-copy">
          <p className="eyebrow">{skill.category}</p>
          <div className="hero-title-row">
            <span className={`hero-skill-icon tone-${skill.color}`}>{skill.icon}</span>
            <h1 className="skill-title-hero">{skill.name}</h1>
          </div>
          <p className="hero-text">{skill.tagline}</p>
          <p className="skill-value">{skill.value}</p>
          <div className="status-strip">
            <span className="status-pill">{skill.status}</span>
            <span className="status-pill subtle">{skill.version}</span>
            <span className="status-pill subtle">{skill.agency}</span>
          </div>
          <div className="hero-actions">
            <a className="button primary" href={skill.repo} target="_blank" rel="noreferrer">
              Ver repo en GitHub
            </a>
            <Link className="button ghost" to="/skills">
              Volver al catalogo
            </Link>
          </div>
        </div>
        <div className="skill-hero-meta">
          <MetaRow label="Organismo" value={skill.agency} />
          <MetaRow label="Marco" value={skill.law} />
          <MetaRow label="Version" value={skill.version} />
          <MetaRow label="Estado" value={skill.status} />
          <MetaRow label="Madurez" value={skill.maturity} />
          <MetaRow label="Tipo" value={skill.type} />
        </div>
      </section>

      <section className="section">
        <div className="detail-route-grid">
          <article className="detail-panel">
            <div className="detail-columns">
              <DetailBlock title="Inputs esperados" items={skill.inputs} />
              <DetailBlock title="Outputs principales" items={skill.outputs} />
            </div>
            <div className="detail-columns">
              <div className="detail-block">
                <h4>Para quien sirve</h4>
                <p>{skill.audience}</p>
              </div>
              <DetailBlock title="Tags" items={skill.tags} />
            </div>
            <div className="detail-columns">
              <div className="detail-block">
                <h4>Que destraba</h4>
                <p>{skill.value}</p>
              </div>
              <div className="detail-block">
                <h4>Relacion dentro del sistema</h4>
                <p>
                  Esta skill forma parte del cluster <strong>{skill.category}</strong> y se vincula con
                  otras piezas del ecosistema para cubrir el flujo completo.
                </p>
                <div className="card-actions">
                  <a className="mini-link" href={skill.repo} target="_blank" rel="noreferrer">
                    Abrir repositorio
                  </a>
                </div>
              </div>
            </div>
          </article>
          <aside className="detail-side">
            <div className="mini-panel">
              <span className="panel-label">Relacionadas</span>
              <div className="related-list">
                {related.map((item) => (
                  <Link className="related-chip" key={item.slug} to={`/skills/${item.slug}`}>
                    {item.name}
                  </Link>
                ))}
              </div>
            </div>
          </aside>
        </div>
      </section>
    </>
  );
}

function CategoriesPage() {
  return (
    <section className="section">
      <SectionHeading
        eyebrow="Categorias"
        title="Navegacion por problema"
        copy="Cada categoria actua como un carril tematico dentro del ecosistema."
      />
      <div className="category-grid">
        {Object.entries(categorySummaries).map(([name, summary]) => (
          <article className="category-card" key={name}>
            <div className="category-card-topline">
              <span className="category-icon">{categoryIcons[name]}</span>
              <span className="panel-label">{skills.filter((skill) => skill.category === name).length} skills</span>
            </div>
            <h3>{name}</h3>
            <p>{summary}</p>
            <ul>
              {skills
                .filter((skill) => skill.category === name)
                .map((skill) => (
                  <li key={skill.slug}>{skill.name}</li>
                ))}
            </ul>
            <div className="card-actions">
              <Link className="mini-link" to={`/categorias/${categorySlugs[name]}`}>
                Explorar cluster
              </Link>
              {skills
                .filter((skill) => skill.category === name)
                .slice(0, 1)
                .map((skill) => (
                  <a className="mini-link subtle" href={skill.repo} key={skill.slug} target="_blank" rel="noreferrer">
                    Repo ejemplo
                  </a>
                ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function CategoryPage() {
  const { slug } = useParams();
  const entry = Object.entries(categorySlugs).find(([, value]) => value === slug);
  if (!entry) {
    return <Navigate to="/categorias" replace />;
  }
  const [name] = entry;
  const list = skills.filter((skill) => skill.category === name);

  return (
    <section className="section">
      <SectionHeading
        eyebrow="Categoria"
        title={name}
        copy={categorySummaries[name]}
      />
      <div className="skills-grid">
        {list.map((skill) => (
          <SkillCard key={skill.slug} skill={skill} />
        ))}
      </div>
    </section>
  );
}

function MapPage() {
  return (
    <section className="section">
      <SectionHeading
        eyebrow="Mapa"
        title="Como se conectan"
        copy="Esta vista transforma la coleccion en una topologia de trabajo: preparacion, contrato, registro, expansion y QA."
      />
      <div className="map-shell">
        {mapColumns.map((column) => (
          <article className="map-column" key={column.title}>
            <h3>{column.title}</h3>
            <div className="map-flow">
              {column.nodes.map((slug, index) => {
                const skill = getSkill(slug);
                return (
                  <React.Fragment key={slug}>
                    <Link className={`map-node tone-${skill.color}`} to={`/skills/${skill.slug}`}>
                      <strong>{skill.name}</strong>
                      <span>{skill.agency}</span>
                    </Link>
                    {index < column.nodes.length - 1 ? <div className="map-arrow">↓</div> : null}
                  </React.Fragment>
                );
              })}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function FrameworkPage() {
  return (
    <section className="section">
      <SectionHeading
        eyebrow="Framework"
        title="Como esta armado el sistema"
        copy="La consistencia entre repos es parte del valor. Cada skill sigue una misma disciplina operacional."
      />
      <div className="framework-grid">
        {[
          ["01", "Proceso experto", "Cada repo traduce un proceso legal o burocratico a una secuencia operable."],
          ["02", "Evidencia antes que narrativa", "Primero se recolecta informacion real; despues se escriben borradores."],
          ["03", "STOP_FOR_USER", "Los puntos sensibles quedan detenidos para confirmacion humana."],
          ["04", "V2 y V3", "La v2 expande la skill general y la v3 la especializa por vertical."],
        ].map(([index, title, copy]) => (
          <article className="framework-card" key={title}>
            <span className="card-index">{index}</span>
            <h3>{title}</h3>
            <p>{copy}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

function ReposPage() {
  return (
    <section className="section">
      <SectionHeading
        eyebrow="Repos"
        title="Indice de repositorios"
        copy="Cada skill sigue siendo independiente. Esta pagina solo centraliza acceso y contexto."
      />
      <div className="repo-table">
        {skills.map((skill) => (
          <article className="repo-row" key={skill.slug}>
            <div>
              <strong>{skill.name}</strong>
              <p>{skill.tagline}</p>
            </div>
            <div>{skill.category}</div>
            <div>
              <span className="repo-pill">{skill.maturity}</span>
            </div>
            <div>
              <a className="repo-link" href={skill.repo} target="_blank" rel="noreferrer">
                Abrir repo
              </a>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function PathwayCard({ title, steps, tone }) {
  return (
    <article className={`pathway-card tone-${tone}`}>
      <span className="panel-label">Secuencia</span>
      <h3>{title}</h3>
      <div className="pathway-steps">
        {steps.map((step, index) => (
          <React.Fragment key={step}>
            <div className="pathway-step">{step}</div>
            {index < steps.length - 1 ? <div className="pathway-arrow">→</div> : null}
          </React.Fragment>
        ))}
      </div>
    </article>
  );
}

function FeaturedCarousel({ items }) {
  const [activeIndex, setActiveIndex] = React.useState(0);

  React.useEffect(() => {
    const timer = window.setInterval(() => {
      setActiveIndex((current) => (current + 1) % items.length);
    }, 3200);
    return () => window.clearInterval(timer);
  }, [items.length]);

  const active = items[activeIndex];

  return (
    <div className="featured-carousel">
      <span className="panel-label">Skills destacadas</span>
      <article className={`featured-card tone-${active.color}`}>
        <Link className="featured-card-link" to={`/skills/${active.slug}`}>
          <div className="featured-card-head">
            <span className="featured-icon">{active.icon}</span>
            <div className="featured-head-copy">
              <small>{active.agency}</small>
              <strong>{active.name}</strong>
            </div>
          </div>
          <p>{active.value}</p>
        </Link>
        <div className="featured-meta-row">
          <span className="status-pill">{active.status}</span>
          <span className="status-pill subtle">{active.version}</span>
        </div>
      </article>
      <div className="featured-track">
        {items.map((skill, index) => (
          <button
            className={`featured-chip ${index === activeIndex ? "active" : ""}`}
            key={skill.slug}
            onClick={() => setActiveIndex(index)}
            type="button"
          >
            <span>{skill.icon}</span>
            <strong>{skill.name}</strong>
          </button>
        ))}
      </div>
    </div>
  );
}

function SkillCard({ skill }) {
  return (
    <article className={`skill-card tone-${skill.color}`}>
      <Link className="skill-card-link" to={`/skills/${skill.slug}`}>
        <div className="skill-card-top">
          <span className="skill-card-kicker">
            <span className="skill-card-icon">{skill.icon}</span>
            {skill.category}
          </span>
          <span>{skill.agency}</span>
        </div>
        <h3 className="skill-title">{skill.name}</h3>
        <p className="skill-tagline">{skill.tagline}</p>
        <p className="skill-microcopy">{skill.value}</p>
        <div className="status-strip compact">
          <span className="status-pill">{skill.status}</span>
          <span className="status-pill subtle">{skill.version}</span>
        </div>
        <div className="skill-tags">
          {skill.tags.slice(0, 4).map((tag) => (
            <span className="tag" key={tag}>
              {tag}
            </span>
          ))}
        </div>
      </Link>
      <div className="card-actions">
        <Link className="mini-link" to={`/skills/${skill.slug}`}>
          Ver ficha
        </Link>
        <a className="mini-link subtle" href={skill.repo} target="_blank" rel="noreferrer">
          Ver repo
        </a>
      </div>
    </article>
  );
}

function FilterGroup({ title, options, value, onChange }) {
  return (
    <div className="filter-group">
      <span className="filter-title">{title}</span>
      <div className="chip-row">
        {options.map((option) => (
          <button
            key={option}
            className={`chip ${value === option ? "active" : ""}`}
            onClick={() => onChange(option)}
            type="button"
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  );
}

function SectionHeading({ eyebrow, title, copy }) {
  return (
    <div className="section-heading">
      <div>
        <p className="eyebrow">{eyebrow}</p>
        <h2>{title}</h2>
      </div>
      <p className="section-copy">{copy}</p>
    </div>
  );
}

function DetailBlock({ title, items }) {
  return (
    <section className="detail-block">
      <h4>{title}</h4>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  );
}

function Metric({ value, label }) {
  return (
    <div className="metric-card">
      <strong>{value}</strong>
      <span>{label}</span>
    </div>
  );
}

function MetaRow({ label, value }) {
  return (
    <div className="meta-row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

export default App;
