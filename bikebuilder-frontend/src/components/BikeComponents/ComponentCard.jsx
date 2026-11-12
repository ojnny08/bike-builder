import { money, titleCase } from '../../utils/format'
import CategoryIcon from '../Icons/CategoryIcons'
import "../../styles/components/BikeComponents/ComponentCard.css"

const ComponentCard = ({ comp, isSelected, onSelect }) => {

    const selectable = typeof onSelect === "function";
    const blocked = selectable && comp.compatible === false;

      return (
          <button
              type="button"
              className={`product-card${blocked ? " is-blocked" : ""}${isSelected ? " is-selected" : ""}`}
              aria-disabled={blocked}
              onClick={() => selectable && !blocked && onSelect(comp)}
          >
            <div className="product-media">
                {comp.image_url ? (
                    <img src={comp.image_url} alt={comp.name} loading="lazy" />
                ) : (
                    ""
                )}
                {blocked && <span className="product-badge-blocked">Incompatible</span>}
            </div>
            <div className="product-card-body">
                <h1 className="product-brand">{comp.brand}</h1>
                <div className="product-name-row">
                    <p className="product-name">{comp.name}</p>
                    <div className="product-price">{money(comp.price)}</div>
                </div>

                {comp.description && (
                    <p className="product-desc">{comp.description}</p>
                )}
            </div>
            <div className="product-card-footer">
            </div>
        </button>
    )
}

const PLACEHOLDERS = {
    skipped: { brand: () => "None", name: label => `No ${label}`, price: money(0) },
    unknown: { brand: label => `Unknown ${label}`, name: () => "Select if you're not sure", price: "" },
};

export const PlaceholderCard = ({ category, kind, isSelected, onClick }) => {
    const meta = PLACEHOLDERS[kind];
    return (
        <button
            type="button"
            className={`product-card is-placeholder${isSelected ? " is-selected" : ""}`}
            onClick={onClick}
        >
            <div className="product-media">
                <span className="product-skip-icon">
                    <CategoryIcon category={category} />
                    {kind === "skipped" && (
                        <svg className="product-skip-cross" viewBox="0 0 64 64" aria-hidden="true">
                            <circle cx="32" cy="32" r="28" />
                            <path d="M12 52L52 12" />
                        </svg>
                    )}
                </span>
            </div>
            <div className="product-card-body">
                <h1 className="product-brand">{meta.brand(titleCase(category).toLowerCase())}</h1>
                <div className="product-name-row">
                    <p className="product-name">{meta.name(titleCase(category).toLowerCase())}</p>
                    <div className="product-price">{meta.price}</div>
                </div>
            </div>
            <div className="product-card-footer">
            </div>
        </button>
    );
};

export const ComponentCardSkeleton = () => (
    <div className="product-card is-skeleton" aria-hidden="true">
        <div className="product-media" />
        <div className="product-card-body">
            <span className="skeleton product-skeleton-line product-skeleton-line--brand" />
            <span className="skeleton product-skeleton-line product-skeleton-line--name" />
        </div>
        <div className="product-card-footer">
            <span className="skeleton product-skeleton-line product-skeleton-line--price" />
        </div>
    </div>
);

export default ComponentCard;