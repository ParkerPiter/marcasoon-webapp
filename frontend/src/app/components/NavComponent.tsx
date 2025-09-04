
function NavComponent() {
  return (
    <nav>
        <div className="flex gap-4 text-black">
            <p><a href="/">Home</a></p>
            <p><a href="/about">About</a></p>
            <p><a href="/contact">Contact</a></p>
        </div>
    </nav>
  );
}

export default NavComponent;