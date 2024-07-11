from selenium.webdriver.common.by import By


class XPaths:
    INVENTORY_LIST = (By.CSS_SELECTOR, "div.inventory_list")
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    RESET_APP_STATE = (By.ID, "reset_sidebar_link")
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
    DIV_TEXT_EQUALS = "//div[text()='{product_name}']"
    DIV_CLASS_EQUALS = "//div[@class='{css}']"
    BACK_TO_PRODUCTS_BUTTON = (By.CLASS_NAME, "inventory_details_back_button")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    ZIP_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    PRODUCT_BUTTON_IN_CHECKOUT = "//div[text()='{product_name}']/../../div[@class='item_pricebar']//button"
    PRODUCT_PRICE_IN_CHECKOUT = "//div[text()='{product_name}']/../../div[@class='item_pricebar']//div"
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message-container")
    CART_ITEM_NAME = "//div[@class='inventory_item_name']"
    CART_ITEM_PRICE = "//div[@class='inventory_item_price']"
    CANCEL_BUTTON = (By.ID, "cancel")
