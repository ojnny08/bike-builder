import './ComponentCard.css'

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
                <p className="product-name">{comp.name}</p>
                <div className="product-meta">
                    <div className="product-price">${comp.price}</div>
                    <div className="product-weight">{comp.weight_grams}g</div>
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

export const ComponentCardSkeleton = () => (
    <div className="product-card is-skeleton" aria-hidden="true">
        <div className="product-media" />
        <div className="product-card-body">
            <span className="skeleton-line skeleton-line--brand" />
            <span className="skeleton-line skeleton-line--name" />
        </div>
        <div className="product-card-footer">
            <span className="skeleton-line skeleton-line--price" />
        </div>
    </div>
);

export default ComponentCard;