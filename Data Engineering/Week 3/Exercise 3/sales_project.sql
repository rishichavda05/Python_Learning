--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

-- Started on 2026-08-23 16:22:42

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 16735)
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    category_id integer NOT NULL,
    category_name character varying(100)
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16730)
-- Name: customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers (
    customer_id integer NOT NULL,
    customer_name character varying(100),
    city character varying(100),
    country character varying(100)
);


ALTER TABLE public.customers OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16810)
-- Name: dim_customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dim_customer (
    customer_id integer NOT NULL,
    customer_name character varying(100),
    city character varying(100),
    country character varying(100)
);


ALTER TABLE public.dim_customer OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16825)
-- Name: dim_date; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dim_date (
    date_id integer NOT NULL,
    full_date date,
    day integer,
    month integer,
    year integer
);


ALTER TABLE public.dim_date OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16820)
-- Name: dim_product; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dim_product (
    product_id integer NOT NULL,
    product_name character varying(100),
    category_name character varying(100),
    price numeric(10,2)
);


ALTER TABLE public.dim_product OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16815)
-- Name: dim_store; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dim_store (
    store_id integer NOT NULL,
    store_name character varying(100),
    city character varying(100)
);


ALTER TABLE public.dim_store OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16830)
-- Name: fact_sales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fact_sales (
    sales_id integer NOT NULL,
    order_id integer,
    customer_id integer,
    product_id integer,
    store_id integer,
    date_id integer,
    quantity integer,
    unit_price numeric(10,2),
    sales_amount numeric(10,2)
);


ALTER TABLE public.fact_sales OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16770)
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    order_item_id integer NOT NULL,
    order_id integer,
    product_id integer,
    quantity integer,
    unit_price numeric(10,2)
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16755)
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    order_id integer NOT NULL,
    customer_id integer,
    store_id integer,
    order_date date
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16740)
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    product_id integer NOT NULL,
    product_name character varying(100),
    category_id integer,
    price numeric(10,2)
);


ALTER TABLE public.products OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16750)
-- Name: stores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stores (
    store_id integer NOT NULL,
    store_name character varying(100),
    city character varying(100)
);


ALTER TABLE public.stores OWNER TO postgres;

--
-- TOC entry 4911 (class 0 OID 16735)
-- Dependencies: 218
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (category_id, category_name) FROM stdin;
1	Electronics
2	Furniture
3	Accessories
\.


--
-- TOC entry 4910 (class 0 OID 16730)
-- Dependencies: 217
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customers (customer_id, customer_name, city, country) FROM stdin;
1	Rahul	Ahmedabad	India
2	Priya	Mumbai	India
3	Amit	Delhi	India
4	Neha	Pune	India
\.


--
-- TOC entry 4916 (class 0 OID 16810)
-- Dependencies: 223
-- Data for Name: dim_customer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dim_customer (customer_id, customer_name, city, country) FROM stdin;
1	Rahul	Ahmedabad	India
2	Priya	Mumbai	India
3	Amit	Delhi	India
4	Neha	Pune	India
\.


--
-- TOC entry 4919 (class 0 OID 16825)
-- Dependencies: 226
-- Data for Name: dim_date; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dim_date (date_id, full_date, day, month, year) FROM stdin;
1	2026-01-10	10	1	2026
2	2026-01-15	15	1	2026
3	2026-02-05	5	2	2026
4	2026-02-10	10	2	2026
5	2026-02-15	15	2	2026
\.


--
-- TOC entry 4918 (class 0 OID 16820)
-- Dependencies: 225
-- Data for Name: dim_product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dim_product (product_id, product_name, category_name, price) FROM stdin;
1	Laptop	Electronics	60000.00
2	Mobile	Electronics	30000.00
3	Chair	Furniture	5000.00
4	Mouse	Accessories	1000.00
5	Keyboard	Accessories	2000.00
\.


--
-- TOC entry 4917 (class 0 OID 16815)
-- Dependencies: 224
-- Data for Name: dim_store; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dim_store (store_id, store_name, city) FROM stdin;
1	Ahmedabad Store	Ahmedabad
2	Mumbai Store	Mumbai
3	Delhi Store	Delhi
\.


--
-- TOC entry 4920 (class 0 OID 16830)
-- Dependencies: 227
-- Data for Name: fact_sales; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fact_sales (sales_id, order_id, customer_id, product_id, store_id, date_id, quantity, unit_price, sales_amount) FROM stdin;
1	101	1	1	1	1	1	60000.00	60000.00
2	101	1	4	1	1	2	1000.00	2000.00
3	102	2	2	2	2	1	30000.00	30000.00
4	102	2	5	2	2	1	2000.00	2000.00
5	103	3	3	3	3	2	5000.00	10000.00
6	104	1	4	1	4	3	1000.00	3000.00
7	105	4	1	2	5	1	60000.00	60000.00
\.


--
-- TOC entry 4915 (class 0 OID 16770)
-- Dependencies: 222
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_items (order_item_id, order_id, product_id, quantity, unit_price) FROM stdin;
1	101	1	1	60000.00
2	101	4	2	1000.00
3	102	2	1	30000.00
4	102	5	1	2000.00
5	103	3	2	5000.00
6	104	4	3	1000.00
7	105	1	1	60000.00
\.


--
-- TOC entry 4914 (class 0 OID 16755)
-- Dependencies: 221
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (order_id, customer_id, store_id, order_date) FROM stdin;
101	1	1	2026-01-10
102	2	2	2026-01-15
103	3	3	2026-02-05
104	1	1	2026-02-10
105	4	2	2026-02-15
\.


--
-- TOC entry 4912 (class 0 OID 16740)
-- Dependencies: 219
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (product_id, product_name, category_id, price) FROM stdin;
1	Laptop	1	60000.00
2	Mobile	1	30000.00
3	Chair	2	5000.00
4	Mouse	3	1000.00
5	Keyboard	3	2000.00
\.


--
-- TOC entry 4913 (class 0 OID 16750)
-- Dependencies: 220
-- Data for Name: stores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stores (store_id, store_name, city) FROM stdin;
1	Ahmedabad Store	Ahmedabad
2	Mumbai Store	Mumbai
3	Delhi Store	Delhi
\.


--
-- TOC entry 4737 (class 2606 OID 16739)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_id);


--
-- TOC entry 4735 (class 2606 OID 16734)
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (customer_id);


--
-- TOC entry 4747 (class 2606 OID 16814)
-- Name: dim_customer dim_customer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dim_customer
    ADD CONSTRAINT dim_customer_pkey PRIMARY KEY (customer_id);


--
-- TOC entry 4753 (class 2606 OID 16829)
-- Name: dim_date dim_date_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dim_date
    ADD CONSTRAINT dim_date_pkey PRIMARY KEY (date_id);


--
-- TOC entry 4751 (class 2606 OID 16824)
-- Name: dim_product dim_product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dim_product
    ADD CONSTRAINT dim_product_pkey PRIMARY KEY (product_id);


--
-- TOC entry 4749 (class 2606 OID 16819)
-- Name: dim_store dim_store_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dim_store
    ADD CONSTRAINT dim_store_pkey PRIMARY KEY (store_id);


--
-- TOC entry 4755 (class 2606 OID 16834)
-- Name: fact_sales fact_sales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fact_sales
    ADD CONSTRAINT fact_sales_pkey PRIMARY KEY (sales_id);


--
-- TOC entry 4745 (class 2606 OID 16774)
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (order_item_id);


--
-- TOC entry 4743 (class 2606 OID 16759)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);


--
-- TOC entry 4739 (class 2606 OID 16744)
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);


--
-- TOC entry 4741 (class 2606 OID 16754)
-- Name: stores stores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_pkey PRIMARY KEY (store_id);


--
-- TOC entry 4761 (class 2606 OID 16835)
-- Name: fact_sales fact_sales_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fact_sales
    ADD CONSTRAINT fact_sales_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.dim_customer(customer_id);


--
-- TOC entry 4762 (class 2606 OID 16850)
-- Name: fact_sales fact_sales_date_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fact_sales
    ADD CONSTRAINT fact_sales_date_id_fkey FOREIGN KEY (date_id) REFERENCES public.dim_date(date_id);


--
-- TOC entry 4763 (class 2606 OID 16840)
-- Name: fact_sales fact_sales_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fact_sales
    ADD CONSTRAINT fact_sales_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.dim_product(product_id);


--
-- TOC entry 4764 (class 2606 OID 16845)
-- Name: fact_sales fact_sales_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fact_sales
    ADD CONSTRAINT fact_sales_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.dim_store(store_id);


--
-- TOC entry 4759 (class 2606 OID 16775)
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(order_id);


--
-- TOC entry 4760 (class 2606 OID 16780)
-- Name: order_items order_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);


--
-- TOC entry 4757 (class 2606 OID 16760)
-- Name: orders orders_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- TOC entry 4758 (class 2606 OID 16765)
-- Name: orders orders_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(store_id);


--
-- TOC entry 4756 (class 2606 OID 16745)
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(category_id);


-- Completed on 2026-08-23 16:22:46

--
-- PostgreSQL database dump complete
--

