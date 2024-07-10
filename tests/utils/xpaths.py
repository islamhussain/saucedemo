from selenium.webdriver.common.by import By


class XPaths:
    INVENTORY_LIST = (By.CSS_SELECTOR, "div.inventory_list")
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    BURGER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_SIDEBAR_LINK = (By.ID, "logout_sidebar_link")
    CART_BADGE = (By.CSS_SELECTOR, "span.shopping_cart_badge")
    REMOVE_BACKPACK_BUTTON = (By.CSS_SELECTOR, "button[data-test='remove-sauce-labs-backpack']")
    ADD_BACKPACK_BUTTON = (By.CSS_SELECTOR, "button[data-test='add-to-cart-sauce-labs-backpack']")
    PRODUCT_BUTTON = "//div[text()='{product_name}']/../../..//button"
    REMOVE_PRODUCT_BUTTON = "//div[text()='{product_name}']/../../../descendant::button"
    PRODUCT_PRICE = "//div[text()='{product_name}']/../../../div[@class='pricebar']/div"
    PRODUCT_IMAGE = "//div[text()='{product_name}']/../../../../div[@class='inventory_item_img']/a" \
                    "/img[contains(@src,'{product_image}')]"
    PRODUCT_NAME = "//div[text()='{product_name}']"
