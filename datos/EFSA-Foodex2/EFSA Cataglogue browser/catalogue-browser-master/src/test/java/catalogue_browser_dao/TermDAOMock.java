package catalogue_browser_dao;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;

import catalogue.Catalogue;
import catalogue_object.Term;

public class TermDAOMock implements CatalogueEntityDAO<Term> {

	private Collection<Term> database;
	
	public TermDAOMock() {
		this.database = new ArrayList<>();
	}
	
	public void clear() {
		database.clear();
	}

	@Override
	public boolean remove(Term attr) {
		
		Iterator<Term> iterator = database.iterator();
		
		while(iterator.hasNext()) {
			
			Term c = iterator.next();
			
			if (c.getCode().equals(attr.getCode()))
				iterator.remove();
		}
		
		return true;
	}

	@Override
	public int insert(Term object) {
		this.database.add(object);
		return 0;
	}

	@Override
	public boolean update(Term object) {
		this.remove(object);
		this.insert(object);
		return true;
	}

	@Override
	public Term getById(int id) {
		for (Term c : database) {
			if (c.getId() == id)
				return c;
		}
		return null;
	}

	@Override
	public Term getByResultSet(ResultSet rs) throws SQLException {
		
		return null;
	}

	@Override
	public Collection<Term> getAll() {
		return this.database;
	}

	@Override
	public void setCatalogue(Catalogue catalogue) {}

	@Override
	public List<Integer> insert(Iterable<Term> attrs) {
		return null;
	}
}
